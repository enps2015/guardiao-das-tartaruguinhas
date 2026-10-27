"""Pure data-state helpers for Guardião das Tartaruguinhas.

Keep business-state decisions independent from Streamlit so they can be tested
without importing or executing the dashboard UI.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

VALID_RISK_LEVELS = {"🟢", "🟡", "🔴"}


def summarize_risk_data(df: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """Classify whether the available records support a risk conclusion.

    States:
      - no_data: no records to evaluate
      - invalid_schema: records exist but the risk column is absent
      - incomplete_data: at least one risk value is missing/unrecognized
      - critical_alerts: complete risk labels and one or more critical records
      - no_critical_alerts: complete risk labels and no critical records
    """
    if df is None or df.empty:
        return {
            "state": "no_data",
            "total_records": 0,
            "critical_records": None,
            "unknown_risk_records": 0,
        }

    if "risco" not in df.columns:
        return {
            "state": "invalid_schema",
            "total_records": int(len(df)),
            "critical_records": None,
            "unknown_risk_records": int(len(df)),
        }

    risk_values = df["risco"]
    valid_mask = risk_values.isin(VALID_RISK_LEVELS)
    unknown_count = int((~valid_mask).sum())
    critical_count = int((risk_values == "🔴").sum())

    if unknown_count:
        state = "incomplete_data"
    elif critical_count:
        state = "critical_alerts"
    else:
        state = "no_critical_alerts"

    return {
        "state": state,
        "total_records": int(len(df)),
        "critical_records": critical_count,
        "unknown_risk_records": unknown_count,
    }


def save_csv_atomically(df: pd.DataFrame, destination: str | Path) -> None:
    """Write a CSV to a temporary file and atomically replace the destination.

    This prevents readers from observing a partially written CSV if a write is
    interrupted. It does not make local disk storage durable across cloud
    restarts and does not replace a database for concurrent multi-user writes.
    """
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Optional[Path] = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=str(path.parent),
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            df.to_csv(temporary_file, index=False)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, path)
    except Exception:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise
