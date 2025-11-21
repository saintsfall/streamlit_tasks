import streamlit as st
import pandas as pd
import unicodedata
import re
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def normalize_name(name):
    """Normaliza nomes de lojas removendo acentos e espaços."""
    if pd.isna(name):
        return name
    
    name = unicodedata.normalize('NFKD', str(name))
    name = name.encode('ASCII', 'ignore').decode('ASCII')
    name = name.lower().strip()
    name = re.sub(r'\s+', '', name)
    
    return name

def apply_filters(df, task_type, seller_selected):
    """Aplica filtros ao DataFrame."""
    df_filtered = df.copy()
    
    # Filtro de tipo de tarefa
    if task_type == "Tarefas Pai":
        df_filtered = df_filtered[df_filtered["Parent ID"].isna()]
    elif task_type == "Subtarefas":
        df_filtered = df_filtered[df_filtered["Parent ID"].notna()]
    
    # Filtro de seller
    if seller_selected and seller_selected != "Todos":
        df_filtered = df_filtered[df_filtered["Nome da loja (short text)"] == seller_selected]
    
    return df_filtered

# ============================================================================
# FUNÇÕES DE RENDERIZAÇÃO DAS SEÇÕES
# ============================================================================

def render_metrics(df_filtered):
    """Renderiza as métricas principais."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cards = df_filtered.shape[0]
        st.metric("Total de Cards", total_cards)
    
    with col2:
        total_pontos = df_filtered["Pontos de Front (number)"].sum()
        st.metric("Total de Pontos", f"{total_pontos:.0f}" if not pd.isna(total_pontos) else "0")
    
    with col3:
        tarefas_pai = df_filtered[df_filtered["Parent ID"].isna()].shape[0]
        st.metric("Tarefas Pai", tarefas_pai)
    
    with col4:
        subtarefas = df_filtered[df_filtered["Parent ID"].notna()].shape[0]
        st.metric("Subtarefas", subtarefas)
    
    st.divider()

def render_charts(df_filtered):
    """Renderiza os gráficos de barras."""
    # Contagem de tarefas por loja normalizada
    store_count = df_filtered['Nome Normalizado'].value_counts().sort_values(ascending=False)
    
    # Pontos por loja normalizada
    points_by_seller = df_filtered.groupby('Nome Normalizado')['Pontos de Front (number)'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 - Quantidade de Tarefas")
        top_10_tasks = store_count.head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top_10_tasks.index,
                y=top_10_tasks.values,
                text=top_10_tasks.values,
                textposition='inside',
                marker_color='lightblue'
            )
        ])
        
        fig.update_layout(
            xaxis_title="Loja",
            yaxis_title="Quantidade de Tarefas",
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Top 10 - Pontos por Loja")
        top_10_points = points_by_seller.head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top_10_points.index,
                y=top_10_points.values,
                text=top_10_points.values,
                textposition='inside',
                marker_color='lightgreen'
            )
        ])
        
        fig.update_layout(
            xaxis_title="Loja",
            yaxis_title="Pontos",
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
    
    st.divider()
    
    return store_count, points_by_seller

def render_store_analysis(store_count, points_by_seller):
    """Renderiza a análise por loja (apenas quando 'Todos' está selecionado)."""
    st.subheader("Análise por Loja (Nomes Normalizados)")
    
    analysis_df = pd.DataFrame({
        'Nome da loja normalizado': store_count.index,
        'Quantidade de tarefas': store_count.values,
        'Total de pontos': [points_by_seller.get(store, 0) for store in store_count.index]
    })
    
    st.dataframe(analysis_df, width='stretch', height=400)
    st.divider()

def render_all_parent_tasks(df_filtered):
    """Renderiza todas as tarefas pai."""
    st.subheader("Todas as Tarefas Pai")
    
    parent_tasks = df_filtered[df_filtered["Parent ID"].isna()].copy()
    
    if not parent_tasks.empty:
        # Contar quantas subtarefas cada tarefa pai tem
        subtasks_count = df_filtered[df_filtered["Parent ID"].notna()].groupby('Parent ID').size()
        
        # Adicionar coluna com contagem de subtarefas
        parent_tasks['Total_Subtarefas'] = parent_tasks['Task ID'].map(subtasks_count).fillna(0).astype(int)
        
        # Criar URL da tarefa pai baseada no Task ID
        parent_tasks['Task URL'] = parent_tasks['Task ID'].apply(
            lambda task_id: f"https://app.clickup.com/t/{task_id}" if pd.notna(task_id) else ""
        )
        
        # Selecionar colunas relevantes para exibir
        columns_to_show = ['Task URL', 'Task Name', 'Nome da loja (short text)', 
                          'Pontos de Front (number)', 'Total_Subtarefas']
        
        # Filtrar apenas colunas que existem no DataFrame
        available_columns = [col for col in columns_to_show if col in parent_tasks.columns]
        parent_tasks_display = parent_tasks[available_columns].copy()
        
        # Renomear colunas para melhor visualização
        parent_tasks_display.columns = parent_tasks_display.columns.str.replace('_', ' ')
        
        st.dataframe(parent_tasks_display, width='stretch', height=400)
    else:
        st.info("Nenhuma tarefa pai encontrada com os filtros aplicados.")
    
    st.divider()

def render_parent_with_subtasks(df_filtered):
    """Renderiza cards pai com suas subtarefas."""
    st.subheader("Cards Pai com suas Subtarefas")
    
    if df_filtered["Parent ID"].notna().any():
        subtasks = df_filtered[df_filtered["Parent ID"].notna()].copy()
        
        # Criar URL da subtask baseado no Task ID
        subtasks['Task URL'] = subtasks['Task ID'].apply(
            lambda task_id: f"https://app.clickup.com/t/{task_id}"
        )

        # Ordenar por Task ID
        subtasks = subtasks.sort_values(['Task ID', 'Task Name'])

        # Selecionar colunas relevantes a serem exibidas
        columns_to_show = [
            'Parent URL',
            'Parent Name',
            'Task Name',
            'Task URL',
            'Nome da loja (short text)',
            'Pontos de Front (number)'
        ]

        # Filtrar apenas colunas que existem no DataFrame
        available_columns = [col for col in columns_to_show if col in subtasks.columns]
        subtasks_display = subtasks[available_columns].copy()

        st.dataframe(subtasks_display, width='stretch', height=400)
    else:
        st.info("Nenhuma subtarefa encontrada com os filtros aplicados.")
    
    st.divider()

def render_filtered_data(df_filtered):
    """Renderiza a tabela completa dos dados filtrados."""
    st.subheader("Dados Filtrados")
    st.dataframe(df_filtered, width='stretch', height=400)

# ============================================================================
# CONFIGURAÇÃO DA ORDEM DAS SEÇÕES
# ============================================================================

# Defina aqui a ordem e quais seções devem ser exibidas
# Cada item é uma tupla: (nome_da_funcao, condicao_para_exibir)
# A condição pode ser None (sempre exibe) ou uma função lambda que retorna True/False

SECTION_CONFIG = [
    ('metrics', None),  # Sempre exibe
    ('charts', None),   # Sempre exibe
    ('store_analysis', lambda seller: seller == "Todos"),  # Só quando "Todos" está selecionado
    ('all_parent_tasks', None),  # Sempre exibe
    ('parent_with_subtasks', None),  # Sempre exibe
    ('filtered_data', None),  # Sempre exibe
]

# ============================================================================
# CÓDIGO PRINCIPAL
# ============================================================================

with st.sidebar:
    st.title('Analise de dados')
    uploaded_file = st.file_uploader("Adicione o CSV")

seller_selected = None
task_type = None
df = None

# Carregar e processar arquivo
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Nome Normalizado'] = df['Nome da loja (short text)'].apply(normalize_name)
    
    with st.sidebar:
        st.subheader("Filtros")
        task_type = st.radio(
            "Tipo de Card",
            ["Todos", "Tarefas Pai", "Subtarefas"],
            help="Tarefas Pai: cards sem Parent ID\nSubtarefas: cards com Parent ID"
        )
        
        sellers = df["Nome da loja (short text)"].dropna().unique().tolist()
        sellers_sorted = sorted(sellers)
        seller_selected = st.selectbox('Seller', ["Todos"] + sellers_sorted)

# Renderizar seções
if uploaded_file is not None and df is not None:
    df_filtered = apply_filters(df, task_type, seller_selected)
    store_count = None
    points_by_seller = None
    
    # Renderizar cada seção na ordem definida
    for section_name, condition in SECTION_CONFIG:
        # Verificar se deve exibir a seção
        if condition is not None and not condition(seller_selected):
            continue
        
        # Renderizar a seção correspondente
        if section_name == 'metrics':
            render_metrics(df_filtered)
        elif section_name == 'charts':
            store_count, points_by_seller = render_charts(df_filtered)
        elif section_name == 'store_analysis':
            if store_count is not None and points_by_seller is not None:
                render_store_analysis(store_count, points_by_seller)
        elif section_name == 'all_parent_tasks':
            render_all_parent_tasks(df_filtered)
        elif section_name == 'parent_with_subtasks':
            render_parent_with_subtasks(df_filtered)
        elif section_name == 'filtered_data':
            render_filtered_data(df_filtered)