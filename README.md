# Análise de Dados - Streamlit App

Aplicação Streamlit para análise de dados de tarefas e pautas de frontend.

## 🚀 Funcionalidades

- **Upload de arquivos CSV**: Carregue seus dados via interface
- **Filtros dinâmicos**: 
  - Filtro por tipo de card (Todos, Tarefas Pai, Subtarefas)
  - Filtro por loja/seller
- **Visualizações interativas**:
  - Top 10 - Quantidade de tarefas por loja
  - Top 10 - Pontos por loja
  - Métricas principais (Total de Cards, Pontos, Tarefas Pai, Subtarefas)
- **Análise detalhada**:
  - Tabela com todas as tarefas pai
  - Cards pai com suas subtarefas
  - Análise por loja com nomes normalizados

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd streamlit_tasks
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como executar

Execute o comando:
```bash
streamlit run app/main.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
streamlit_tasks/
├── app/
│   └── main.py          # Aplicação principal
├── data/                # Arquivos de dados CSV (opcional)
├── .streamlit/
│   └── config.toml      # Configurações do Streamlit
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## 📦 Dependências

- `streamlit`: Framework para criação da aplicação web
- `pandas`: Manipulação e análise de dados
- `plotly`: Criação de gráficos interativos

## 🔧 Deploy no Streamlit Cloud

Este projeto está pronto para deploy no [Streamlit Cloud](https://streamlit.io/cloud):

1. Faça push do código para um repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório GitHub
4. Selecione o branch e o arquivo principal: `app/main.py`
5. Clique em "Deploy"

## 📝 Formato dos Dados

O arquivo CSV deve conter as seguintes colunas:
- `Task ID`: ID da tarefa
- `Parent ID`: ID da tarefa pai (pode estar vazio para tarefas pai)
- `Parent Name`: Nome da tarefa pai
- `Nome da loja (short text)`: Nome da loja/seller
- `Pontos de Front (number)`: Pontos atribuídos à tarefa

## 👤 Autor

Projeto desenvolvido para análise de dados de tarefas e pautas.

## 📄 Licença

Este projeto está sob a licença MIT.

