**Plano de Implementação: Dashboard Web Interativo (v3)
Projeto:** Guardião das Tartaruguinhas - A Evolução para a Web
**Visão:** Transformar o sistema de monitoramento baseado em terminal em um
dashboard web moderno, interativo e visualmente impactante, aplicando princípios
de neurodesign para criar uma experiência de usuário (UX) intuitiva e que estimule a
análise e o gerenciamento completo do ciclo de vida dos dados.

**1. A Escolha da Stack Tecnológica: O Caminho da Eficiência e Elegância**
A escolha se mantém no **Streamlit** por sua sinergia com Python, velocidade de
desenvolvimento e riqueza de componentes interativos, ideal para nossas
necessidades.
**2. Arquitetura da Solução: Da Memória à Persistência**
    ● **Backend (Lógica Python):** Manteremos todas as nossas funções de cálculo e
       adicionaremos a lógica para exclusão de registros.
    ● **Frontend (Interface Streamlit):** A interface será construída com componentes
       visuais do Streamlit.
    ● **Persistência de Dados:** Manteremos o uso de um arquivo **CSV (ninhos.csv)**
       como nossa base de dados. O ciclo de leitura e escrita será a base para todas
       as operações de criação e exclusão.
**3. Plano de Neuro-Design e Experiência do Usuário (UX)**
    ● **Narrativa e Contexto:** A página "Sobre o Projeto" continua sendo um pilar para
       criar conexão emocional e contextualizar os dados.
    ● **Paleta de Cores e Layout:** Os princípios de design visual (cores temáticas,
       layout em "Z", sidebar para navegação) serão mantidos para garantir uma
       experiência coesa.
    ● **Componentes Visuais para Despertar Sinapses:**
       ○ **Painel de Alerta, Relatórios e Análises:** Utilizaremos os componentes
          st.metric, st.dataframe e gráficos interativos com **Plotly Express** conforme
          planejado.
       ○ **Adicionar Novo Ninho:** A experiência fluida com st.form será mantida.
       ○ **Gerenciamento de Dados: Exclusão de Registros (NOVO):**
          ■ **Interface Dedicada:** Criaremos uma nova página na barra lateral
             chamada 🗑 Gerenciar Ninhos.
          ■ **Seleção Clara:** Nesta página, exibiremos o relatório completo dos
             ninhos. Abaixo da tabela, um seletor (st.selectbox ou st.multiselect)
             permitirá ao usuário escolher o(s) ninho(s) a serem deletados. Para
             facilitar a identificação, cada ninho no seletor será representado por um
             identificador único (ex: "ID 1 - Praia Norte - 102 ovos").
          ■ **Ação e Confirmação (Neurodesign):** Após a seleção, um botão Deletar
             1


```
Ninho(s) Selecionado(s) ficará visível. Ao clicar, para evitar exclusões
acidentais (um erro comum que gera alta frustração), o sistema não
deletará imediatamente. Em vez disso, exibirá uma caixa de aviso
(st.warning) com a pergunta: "Você tem certeza que deseja deletar este
ninho? Esta ação não pode ser desfeita." Dentro desta caixa, haverá um
botão final: 🔴 Confirmar Exclusão. Somente o clique neste segundo
botão acionará a lógica de exclusão. Este processo de duas etapas é
uma prática de UX fundamental para ações destrutivas.
■ Feedback de Sucesso: Após a exclusão, o sistema exibirá uma
mensagem de sucesso (st.success("Ninho deletado com sucesso!")) e a
página será automaticamente recarregada, mostrando a tabela de dados
atualizada.
```
**4. Fluxo de Exclusão de Dados**
    1. O usuário navega para a página "Gerenciar Ninhos".
    2. Seleciona um ou mais ninhos na lista de seleção.
    3. Clica no botão "Deletar Ninho(s) Selecionado(s)".
    4. O sistema exibe a mensagem de confirmação.
    5. O usuário clica em "Confirmar Exclusão".
    6. A lógica do backend remove a(s) linha(s) correspondente(s) do DataFrame em
       memória.
    7. O sistema imediatamente **sobrescreve** o arquivo ninhos.csv com o DataFrame
       atualizado.
    8. A página é recarregada, refletindo a remoção do dado.
       2


