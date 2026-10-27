import pandas as pd

from guardiao_data import save_csv_atomically, summarize_risk_data


def test_empty_dataset_is_not_interpreted_as_no_risk():
    result = summarize_risk_data(pd.DataFrame(columns=["risco"]))

    assert result["state"] == "no_data"
    assert result["total_records"] == 0
    assert result["critical_records"] is None


def test_no_critical_alerts_requires_complete_risk_classification():
    df = pd.DataFrame({"risco": ["🟢", "🟡", "🟢"]})

    result = summarize_risk_data(df)

    assert result["state"] == "no_critical_alerts"
    assert result["total_records"] == 3
    assert result["critical_records"] == 0
    assert result["unknown_risk_records"] == 0


def test_critical_records_are_counted():
    df = pd.DataFrame({"risco": ["🟢", "🔴", "🔴", "🟡"]})

    result = summarize_risk_data(df)

    assert result["state"] == "critical_alerts"
    assert result["critical_records"] == 2
    assert result["unknown_risk_records"] == 0


def test_missing_or_unrecognized_risk_blocks_no_risk_conclusion():
    df = pd.DataFrame({"risco": ["🟢", None, "revisar"]})

    result = summarize_risk_data(df)

    assert result["state"] == "incomplete_data"
    assert result["total_records"] == 3
    assert result["critical_records"] == 0
    assert result["unknown_risk_records"] == 2


def test_critical_alert_is_still_reported_when_other_risks_are_unknown():
    df = pd.DataFrame({"risco": ["🔴", None]})

    result = summarize_risk_data(df)

    assert result["state"] == "incomplete_data"
    assert result["critical_records"] == 1
    assert result["unknown_risk_records"] == 1


def test_nonempty_dataset_without_risk_column_is_invalid_schema():
    df = pd.DataFrame({"status": ["intacto"], "quantidade_ovos": [50]})

    result = summarize_risk_data(df)

    assert result["state"] == "invalid_schema"
    assert result["total_records"] == 1
    assert result["unknown_risk_records"] == 1


def test_csv_write_is_atomic_and_creates_destination_directory(tmp_path):
    destination = tmp_path / "nested" / "data" / "ninhos.csv"
    original = pd.DataFrame(
        [
            {
                "regiao": "Praia Norte",
                "quantidade_ovos": 80,
                "status": "intacto",
                "risco": "🟢",
                "dias_para_eclosao": 12,
                "predadores": False,
                "causa_risco": "nenhuma",
            }
        ]
    )

    save_csv_atomically(original, destination)

    assert destination.exists()
    reloaded = pd.read_csv(destination)
    assert reloaded.to_dict("records") == original.to_dict("records")
    assert list(destination.parent.glob("*.tmp")) == []
    assert list(destination.parent.glob(".*.tmp")) == []
