# =============================================================================
# GUARDIÃO DAS TARTARUGUINHAS - DASHBOARD WEB
#
# Desenvolvido por: Eric Narciso Pimentel dos Santos
# Mentor: Prof. Ezra M. Kael
# Versão: 2.0 - Streamlit (Evolução)
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------
# SEÇÃO 0: CONFIGURAÇÃO DA PÁGINA E CONSTANTES
# ----------------------------------------------------------------------------

# Configuração inicial da página (deve ser o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Guardião das Tartaruguinhas",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constantes e Regras de Negócio ---
OVOS_MIN_REALISTA = 5
OVOS_MAX_REALISTA = 200
DIAS_ECLOSAO_MIN = 1
DIAS_ECLOSAO_MAX = 130
CAMINHO_DADOS = Path("./data/ninhos.csv")
CAMINHO_LOGO = Path("assets/logo3.png")

# ----------------------------------------------------------------------------
# SEÇÃO 1: FUNÇÕES DE GERENCIAMENTO DE DADOS (PERSISTÊNCIA)
# ----------------------------------------------------------------------------

def carregar_dados():
    """Lê os dados do arquivo CSV. Se o arquivo não existir, cria um DataFrame vazio."""
    if CAMINHO_DADOS.exists():
        df = pd.read_csv(CAMINHO_DADOS)
        # Garante que os tipos de dados estejam corretos após a leitura
        df['quantidade_ovos'] = df['quantidade_ovos'].astype(int)
        df['dias_para_eclosao'] = df['dias_para_eclosao'].astype(int)
        df['predadores'] = df['predadores'].astype(bool)
        return df
    else:
        # Define as colunas para o caso de um arquivo novo
        return pd.DataFrame(columns=[
            "regiao", "quantidade_ovos", "status", "risco", 
            "dias_para_eclosao", "predadores", "causa_risco"
        ])

def salvar_dados(df):
    """Salva o DataFrame atual no arquivo CSV, sobrescrevendo a versão antiga."""
    df.to_csv(CAMINHO_DADOS, index=False)

# ----------------------------------------------------------------------------
# SEÇÃO 2: PÁGINAS E COMPONENTES VISUAIS DO DASHBOARD
# ----------------------------------------------------------------------------

def pagina_sobre():
    """Exibe a página com a narrativa do projeto."""
    st.image(str(CAMINHO_LOGO), width=200)
    st.title("Guardião das Tartaruguinhas")
    st.markdown("---")
    
    st.header("1. Contexto do Projeto")
    st.markdown("""
    Em uma comunidade ribeirinha no coração da Amazônia, um esforço coletivo e inspirador de conservação dos quelônios ganha vida. 
    Liderado por professores e jovens voluntários, o projeto **Guardião das Tartaruguinhas** visa monitorar os ninhos de tartarugas 
    para garantir que o maior número possível de filhotes chegue com segurança ao rio, fortalecendo o ciclo de preservação e a cultura local.
    """)

    st.header("2. O Desafio")
    st.markdown("""
    Os dados dos ninhos eram registrados manualmente em papel, resultando em informações desorganizadas e de difícil análise. 
    Responder a perguntas essenciais para a tomada de decisão tornava-se uma tarefa árdua e imprecisa.
    """)

    st.header("3. A Solução Proposta")
    st.markdown("""
    Este dashboard representa a solução tecnológica para o desafio. É um sistema robusto que permite aos voluntários:
    - **Registrar** os dados de forma padronizada.
    - **Validar** as informações no momento da entrada.
    - **Analisar** os dados acumulados para gerar insights acionáveis.
    - **Apoiar** a tomada de decisão para otimizar os esforços de conservação.
    """)
    
    st.info("> Nosso desafio não é apenas contar os ovos. É usar cada número, cada dado, para tecer uma rede de proteção em torno da vida. Aqui, cada linha de código é um ato de esperança.")

def pagina_painel_alerta(df):
    """Exibe a Central de Monitoramento de Riscos."""
    st.title("Central de Monitoramento de Riscos")
    st.markdown("Análise de alta prioridade para a proteção dos ninhos. *Os dados aqui são sempre do **dataset completo**.*")

    if df.empty:
        st.success("✅ Missão Cumprida! Nenhum ninho em situação de alerta no momento.")
        return

    st.markdown("---")

    # --- MÉTRICAS PRINCIPAIS ---
    col1, col2, col3 = st.columns(3)
    
    # KPI 1: Ninhos em Risco Crítico
    ninhos_risco_critico = df[df["risco"] == "🔴"]
    col1.metric(
        label="Ninhos em Risco Crítico (🔴)",
        value=ninhos_risco_critico.shape[0],
        help="Ninhos que necessitam de intervenção imediata."
    )

    # KPI 2: Eclosão Urgente
    ninhos_eclosao_urgente = df[df["dias_para_eclosao"] <= 2]
    col2.metric(
        label="Eclosão Iminente (em até 48h)",
        value=ninhos_eclosao_urgente.shape[0],
        help="Ninhos que estão prestes a eclodir. Acompanhamento intensificado necessário."
    )
    
    # KPI 3: Taxa de Ninhos Intactos
    total_ninhos = len(df)
    ninhos_intactos = df[df["status"] == "intacto"].shape[0]
    taxa_intactos = (ninhos_intactos / total_ninhos) * 100 if total_ninhos > 0 else 0
    col3.metric(
        label="Taxa de Ninhos Intactos",
        value=f"{taxa_intactos:.1f}%",
        help="Percentual de ninhos que não sofreram ameaças ou danos."
    )

    st.markdown("---")
    st.header("Análise Contextual dos Alertas")

    # --- ANÁLISE CONTEXTUAL ---
    col_grafico1, col_grafico2 = st.columns(2)

    # Paleta de cores com tons de verde e azul
    color_palette = px.colors.sequential.Aggrnyl

    with col_grafico1:
        st.subheader("Regiões com Ninhos Críticos")
        if not ninhos_risco_critico.empty:
            contagem_regiao_critica = ninhos_risco_critico['regiao'].value_counts().reset_index()
            contagem_regiao_critica.columns = ['Região', 'Nº de Ninhos Críticos']
            fig = px.bar(
                contagem_regiao_critica, 
                x='Nº de Ninhos Críticos', 
                y='Região', 
                orientation='h',
                title="Focos de Risco Crítico por Região",
                color='Nº de Ninhos Críticos',
                color_continuous_scale=color_palette
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum ninho em risco crítico para exibir.")

    with col_grafico2:
        st.subheader("Causas de Risco (Ninhos Danificados)")
        df_danificados = df[df['status'] == 'danificado']
        if not df_danificados.empty:
            causas_risco = df_danificados['causa_risco'].value_counts().reset_index()
            causas_risco.columns = ['Causa', 'Contagem']
            fig_causas = px.pie(
                causas_risco, 
                names='Causa', 
                values='Contagem', 
                title="Principais Ameaças aos Ninhos",
                hole=.3,
                color_discrete_sequence=color_palette
            )
            st.plotly_chart(fig_causas, use_container_width=True)
        else:
            st.info("Nenhum ninho danificado para analisar as causas.")

def pagina_relatorio_completo(df):
    """Exibe uma galeria de fichas de monitoramento para cada ninho."""
    st.title("Fichas de Monitoramento de Ninhos")
    
    if df.empty:
        st.warning("Nenhum ninho registrado para exibir no relatório.")
        return

    st.markdown("---")
    
    # --- MÉTRICAS GLOBAIS DO RELATÓRIO ---
    st.header("Visão Geral do Relatório Atual")
    
    total_ninhos_relatorio = len(df)
    total_ovos_relatorio = df['quantidade_ovos'].sum()
    media_ovos_ninho = df['quantidade_ovos'].mean()
    
    try:
        regiao_com_mais_ninhos = df['regiao'].mode()[0]
    except KeyError:
        regiao_com_mais_ninhos = "N/A" # Caso a coluna não exista ou esteja vazia

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Ninhos", f"{total_ninhos_relatorio}")
    col2.metric("Total de Ovos", f"{total_ovos_relatorio}")
    col3.metric("Média de Ovos/Ninho", f"{media_ovos_ninho:.1f}")
    col4.metric("Região com Mais Ninhos", regiao_com_mais_ninhos)

    st.markdown("---")
    st.header("Galeria de Fichas Individuais")

    # Mapeamento de risco para cor da borda
    risco_cor_map = {
        "🟢": "green",
        "🟡": "gold",
        "🔴": "red"
    }

    # Itera sobre cada ninho no dataframe (filtrado ou não) e cria uma ficha
    for index, ninho in df.iterrows():
        cor_borda = risco_cor_map.get(ninho['risco'], 'grey')
        
        # Usando st.container() com uma borda para criar o efeito de "card"
        with st.container(border=True):
            col_id, col_regiao = st.columns([1, 3])
            
            with col_id:
                st.markdown(f"**ID do Ninho:** `{index}`")
            
            with col_regiao:
                st.markdown(f"**Região:** {ninho['regiao']}")

            st.markdown(f"""
            <div style="border-left: 5px solid {cor_borda}; padding-left: 10px;">
                <p><strong>Status:</strong> {ninho['status'].title()} | <strong>Risco:</strong> {ninho['risco']}</p>
                <p><strong>Quantidade de Ovos:</strong> {ninho['quantidade_ovos']}</p>
                <p><strong>Previsão de Eclosão:</strong> {ninho['dias_para_eclosao']} dias</p>
                <p><strong>Ameaça Principal:</strong> {ninho['causa_risco'].title()}</p>
            </div>
            """, unsafe_allow_html=True)

def pagina_analises(df):
    """Exibe as análises descritiva, diagnóstica e a linha do tempo da eclosão."""
    st.title("🔬 Análises Avançadas e Storytelling")
    if df.empty:
        st.warning("Nenhum dado disponível para análise nos filtros selecionados.")
        return

    # --- SEÇÃO DE STORYTELLING: A JORNADA DA VIDA ---
    st.header("A Jornada da Vida: Linha do Tempo da Eclosão")
    
    df_timeline = df.copy()
    # Garante que a coluna de dias para eclosão seja numérica
    df_timeline['dias_para_eclosao'] = pd.to_numeric(df_timeline['dias_para_eclosao'], errors='coerce')
    df_timeline.dropna(subset=['dias_para_eclosao'], inplace=True)
    df_timeline['dias_para_eclosao'] = df_timeline['dias_para_eclosao'].astype(int)

    # Calcula as datas de início e fim
    today = datetime.now()
    df_timeline['start_date'] = today
    df_timeline['end_date'] = df_timeline['dias_para_eclosao'].apply(lambda days: today + timedelta(days=days))
    
    # Cria um identificador único para cada ninho no eixo Y
    df_timeline['ninho_id'] = [f"Ninho {i} ({row['regiao']})" for i, row in df_timeline.iterrows()]
    
    # Ordena pela data de eclosão para melhor visualização
    df_timeline = df_timeline.sort_values(by='end_date')

    if not df_timeline.empty:
        fig_timeline = px.timeline(
            df_timeline,
            x_start="start_date",
            x_end="end_date",
            y="ninho_id",
            color="risco",
            title="Contagem Regressiva para Eclosão dos Ninhos",
            color_discrete_map={'🟢': 'green', '🟡': 'gold', '🔴': 'red'},
            labels={"risco": "Nível de Risco"}
        )
        fig_timeline.update_yaxes(categoryorder="total ascending") # Garante a ordem
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("Nenhum ninho com previsão de eclosão nos dados filtrados.")

    st.markdown("---")

    # --- ANÁLISES TRADICIONAIS ---
    st.header("Análise Descritiva e Diagnóstica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição por Status")
        fig_status = px.pie(df, names='status', title='Distribuição de Ninhos por Status', hole=.3)
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.subheader("Distribuição por Risco")
        fig_risco = px.pie(df, names='risco', title='Distribuição de Ninhos por Risco', hole=.3,
                         color_discrete_map={'🟢':'green', '🟡':'gold', '🔴':'red'})
        st.plotly_chart(fig_risco, use_container_width=True)

    st.subheader("Ranking de Regiões por Volume de Ninhos")
    contagem_regiao = df['regiao'].value_counts().reset_index()
    contagem_regiao.columns = ['Região', 'Contagem de Ninhos']
    fig_ranking = px.bar(contagem_regiao, x='Região', y='Contagem de Ninhos', title='Total de Ninhos por Região')
    st.plotly_chart(fig_ranking, use_container_width=True)

    st.header("Análise Diagnóstica")
    
    st.subheader("Principal Causa para Ninhos Danificados")
    df_danificados = df[df['status'] == 'danificado']
    if not df_danificados.empty:
        causa_principal = df_danificados['causa_risco'].mode()[0]
        st.info(f"A principal causa de danos é: **{causa_principal.title()}**")
    else:
        st.success("Nenhum ninho danificado registrado.")

def pagina_adicionar_ninho(df):
    """Página com formulário para adicionar um novo ninho."""
    st.title("📝 Adicionar Novo Registro de Ninho")

    with st.form("form_novo_ninho", clear_on_submit=True):
        regiao = st.text_input("Região do Ninho")
        quantidade_ovos = st.number_input("Quantidade de Ovos", min_value=OVOS_MIN_REALISTA, max_value=OVOS_MAX_REALISTA, step=1)
        status = st.selectbox("Status do Ninho", ["intacto", "ameaçado", "danificado"])
        risco = st.selectbox("Risco do Ninho", ["🟢", "🟡", "🔴"])
        dias_para_eclosao = st.number_input("Dias para Eclosão", min_value=DIAS_ECLOSAO_MIN, max_value=DIAS_ECLOSAO_MAX, step=1)
        predadores = st.checkbox("Presença de Predadores")
        causa_risco = st.selectbox("Causa do Risco", ["predador", "alagamento", "humano", "desconhecida", "nenhuma"])
        
        submitted = st.form_submit_button("Registrar Ninho")
        
        if submitted:
            novo_ninho = pd.DataFrame([{
                "regiao": regiao, "quantidade_ovos": quantidade_ovos, "status": status,
                "risco": risco, "dias_para_eclosao": dias_para_eclosao,
                "predadores": predadores, "causa_risco": causa_risco
            }])
            df_atualizado = pd.concat([df, novo_ninho], ignore_index=True)
            salvar_dados(df_atualizado)
            st.success("Sucesso! Novo ninho registrado na base de dados.")

def pagina_gerenciar_ninhos(df):
    """Exibe um painel de gerenciamento interativo para os ninhos."""
    st.title("Painel de Gerenciamento de Ninhos")
    
    if df.empty:
        st.info("Não há ninhos registrados para gerenciar.")
        return

    st.markdown("Abaixo estão todos os ninhos registrados. Use o painel em cada ficha para realizar ações.")
    st.markdown("---")

    # Mapeamento de risco para cor da borda
    risco_cor_map = {
        "🟢": "green",
        "🟡": "gold",
        "🔴": "red"
    }

    # Itera sobre cada ninho e cria uma ficha de gerenciamento
    for index, ninho in df.iterrows():
        cor_borda = risco_cor_map.get(ninho['risco'], 'grey')
        
        with st.container(border=True):
            col_info, col_action = st.columns([3, 1])

            with col_info:
                st.markdown(f"**ID:** `{index}` | **Região:** {ninho['regiao']}")
                st.markdown(f"""
                <div style="border-left: 5px solid {cor_borda}; padding-left: 10px; margin-top: 5px;">
                    <small><strong>Status:</strong> {ninho['status'].title()} | <strong>Risco:</strong> {ninho['risco']} | <strong>Ovos:</strong> {ninho['quantidade_ovos']}</small>
                </div>
                """, unsafe_allow_html=True)

            with col_action:
                with st.expander("Deletar Ninho", expanded=False):
                    st.warning("Atenção! Esta ação é irreversível.")
                    # Usar o índice do ninho como chave para o botão garante que cada botão seja único
                    if st.button("🔴 Confirmar Exclusão", key=f"delete_{index}"):
                        df_atualizado = df.drop(index).reset_index(drop=True)
                        salvar_dados(df_atualizado)
                        st.success(f"Ninho ID {index} deletado.")
                        st.experimental_rerun()

# ----------------------------------------------------------------------------
# SEÇÃO 4: LÓGICA PRINCIPAL E NAVEGAÇÃO
# ----------------------------------------------------------------------------

def main():
    # Carrega os dados no início da execução
    df_ninhos = carregar_dados()

    # --- BARRA LATERAL DE NAVEGAÇÃO E FILTROS ---
    with st.sidebar:
        st.image(str(CAMINHO_LOGO), width=150)
        st.title("Guardião das Tartaruguinhas")

        escolha = option_menu(
            menu_title="Menu Principal",
            options=[
                "Sobre o Projeto", "Painel de Alerta", "Relatório Completo", 
                "Análises Avançadas", "Adicionar Ninho", "Gerenciar Ninhos"
            ],
            icons=[
                "info-circle-fill", "exclamation-triangle-fill", "table", 
                "bar-chart-line-fill", "plus-square-fill", "trash-fill"
            ],
            menu_icon="cast",
            default_index=0,
        )

        # --- FILTROS MULTIDIMENSIONAIS (ALQUIMIA INTERATIVA) ---
        st.markdown("---")
        st.header("🔬 Filtros Interativos")

        df_filtrado = df_ninhos.copy()

        # Apenas mostra filtros se houver dados
        if not df_ninhos.empty:
            # Usar sorted() para uma apresentação mais organizada
            regioes = sorted(df_ninhos['regiao'].unique())
            selected_regioes = st.multiselect("Filtrar por Região", regioes, default=regioes)

            riscos = sorted(df_ninhos['risco'].unique())
            selected_riscos = st.multiselect("Filtrar por Risco", riscos, default=riscos)

            status_list = sorted(df_ninhos['status'].unique())
            selected_status = st.multiselect("Filtrar por Status", status_list, default=status_list)

            # Aplica os filtros ao dataframe
            df_filtrado = df_ninhos[
                df_ninhos['regiao'].isin(selected_regioes) &
                df_ninhos['risco'].isin(selected_riscos) &
                df_ninhos['status'].isin(selected_status)
            ]
        else:
            st.warning("Nenhum dado para filtrar.")

        # --- ASSINATURA DO AUTOR ---
        st.markdown("---")
        assinatura = """
        **Desenvolvido com paixão e a Força dos Dados por:**

        **Eric Pimentel**

        [![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eric-np-santos/)
        [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/enps2015)
        [![Instagram Badge](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/eric.n.pimentel/)
        [![Gmail Badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:enps2006@gmail.com)

        ---

        *✨ Última atualização: 30 de Julho de 2025 ✨*
        """
        st.markdown(assinatura)

    # Dicionário para mapear a escolha do menu para a função correspondente
    # Garante que os nomes correspondem exatamente às 'options' do menu
    paginas = {
        "Sobre o Projeto": pagina_sobre,
        "Painel de Alerta": pagina_painel_alerta,
        "Relatório Completo": pagina_relatorio_completo,
        "Análises Avançadas": pagina_analises,
        "Adicionar Ninho": pagina_adicionar_ninho,
        "Gerenciar Ninhos": pagina_gerenciar_ninhos
    }
    
    # --- RENDERIZAÇÃO DA PÁGINA ESCOLHIDA ---
    # Chama a função correspondente à página, passando o DataFrame apropriado
    if escolha == "Sobre o Projeto":
        paginas[escolha]()
    # Para as páginas de adição, gerenciamento e o painel de alerta,
    # é melhor usar o DF completo para evitar confusão.
    elif escolha in ["Adicionar Ninho", "Gerenciar Ninhos", "Painel de Alerta"]:
        paginas[escolha](df_ninhos)
    else:
        paginas[escolha](df_filtrado)


if __name__ == "__main__":
    main()
