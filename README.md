
# Guardião das Tartaruguinhas - v2.0


🐢 Guardião das Tartaruguinhas

**Um sistema de monitoramento comunitário de ninhos de quelônios, desenvolvido como projeto para o curso de IA Aplicada aos Desafios Socioambientais da Amazônia (I2A2).**

---

## 📜 Sobre o Projeto

Este projeto nasceu da necessidade de uma comunidade ribeirinha na Amazônia de digitalizar e organizar os dados coletados manualmente sobre ninhos de tartarugas. O objetivo é transformar dados brutos em insights acionáveis para otimizar os esforços de conservação, garantindo que mais filhotes cheguem com segurança ao rio.


Bem-vindo à versão 2.0 do **Guardião das Tartaruguinhas**, um dashboard de monitoramento de ninhos de quelônios na Amazônia, reimaginado para oferecer uma experiência de análise de dados mais rica, intuitiva e visualmente impactante.

Este projeto transforma dados brutos de conservação em insights acionáveis, utilizando o poder do Streamlit para criar uma ferramenta que não apenas informa, mas também engaja e capacita os voluntários em campo.

## ✨ Principais Funcionalidades da v2.0

A evolução do dashboard focou em quatro pilares de aprimoramento cognitivo e visual:

1.  **Navegação Moderna:** Um menu lateral com ícones substitui a antiga seleção, tornando a navegação mais rápida e intuitiva.
2.  **Central de Monitoramento de Riscos:** O antigo "Painel de Alerta" foi transformado em um cockpit de ação, com métricas claras e gráficos contextuais que direcionam a atenção para os pontos mais críticos.
3.  **Fichas de Monitoramento:** O relatório de dados brutos deu lugar a uma galeria de "cards" individuais para cada ninho, facilitando a consulta e a avaliação visual rápida.
4.  **Storytelling Visual:** Uma linha do tempo interativa na página de análises conta a história da jornada de cada ninho até a eclosão, transformando dados temporais em uma narrativa poderosa.

## 📸 Screenshots da Nova Interface

| Central de Monitoramento de Riscos | Fichas de Monitoramento |
| :---: | :---: |
| ![Tela 01](assets/screenshots/tela01.png) | ![Tela 02](assets/screenshots/tela02.png) |

| Análises Avançadas e Linha do Tempo | Painel de Gerenciamento Interativo |
| :---: | :---: |
| ![Tela 03](assets/screenshots/tela03.png) | ![Tela 04](assets/screenshots/tela04.png) |

| Filtros Interativos | Formulário de Adição |
| :---: | :---: |
| ![Tela 05](assets/screenshots/tela05.png) | ![Tela 06](assets/screenshots/tela06.png) |

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o dashboard em seu ambiente local.

### 1. Pré-requisitos

- Python 3.8+
- `pip` e `venv`

### 2. Configuração do Ambiente

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

**Crie e ative o ambiente virtual:**

```bash
# Crie o ambiente
python -m venv venv

# Ative no macOS/Linux
source venv/bin/activate

# (ou) Ative no Windows
.\venv\Scripts\activate
```

### 3. Instale as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Execute o Dashboard

Para iniciar a aplicação web interativa, execute o comando:

```bash
streamlit run dashboard.py
```

O Streamlit iniciará um servidor local e abrirá o dashboard no seu navegador padrão.

### Persistência dos registros: limitação importante

O dashboard atual utiliza `data/ninhos.csv` como armazenamento local. A gravação foi tornada atômica para evitar que uma interrupção deixe um CSV parcialmente escrito, mas isso **não transforma o arquivo em armazenamento persistente ou multiusuário**.

No Streamlit Community Cloud, a persistência do filesystem local não é garantida após reinicializações ou novos deploys. Por isso, esta versão deve ser tratada como protótipo demonstrativo; não use o CSV local como fonte oficial de registros de campo. Para operação contínua, a próxima evolução deve integrar um banco ou serviço de armazenamento persistente externo, com credenciais em secrets e política de backup.

### Testes automatizados

Para executar as verificações do estado de risco e da gravação CSV localmente:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
```

O GitHub Actions executa esses testes automaticamente em pull requests e em alterações relevantes na aplicação, nos dados ou nos próprios testes.

## 🛠️ Desenvolvido com

*   **Python:** A linguagem por trás de toda a lógica.
*   **Streamlit:** O framework que dá vida à interface web interativa.
*   **Pandas:** Para a manipulação e análise dos dados.
*   **Plotly:** Para a criação dos gráficos ricos e interativos.
*   **streamlit-option-menu:** Para o menu de navegação moderno.

## 🛠️ Tecnologias Utilizadas

* **Python 3:** A única linguagem utilizada, sem a necessidade de bibliotecas externas, focando nos fundamentos da programação.

---
_Este projeto representa a ponte entre o conhecimento tradicional e a tecnologia acessível, transformando dados em um escudo para a biodiversidade amazônica._

**Desenvolvido com paixão e a Força dos Dados por:**

**Eric Pimentel**

[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eric-np-santos/)
[![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/enps2015)
[![Instagram Badge](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/eric.n.pimentel/)
[![Gmail Badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:enps2006@gmail.com)

---

*✨ Última atualização: 30 de Julho de 2025 ✨*


