import os
import pandas as pd
import zipfile
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =============================
# CONFIG & SESSION STATE
# =============================
st.set_page_config(
    page_title="Sales Pipeline Performance",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'grafico_ativo' not in st.session_state:
    st.session_state.grafico_ativo = "Deals"

# =============================
# CSS — DARK EMERALD THEME
# =============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;800&display=swap');

    :root {
        --bg-base:        #080c0e;
        --bg-card:        #121a1e;
        --border:         #1e3030;
        --accent-em:      #10b981;
        --text-primary:   #e8f4f0;
        --text-secondary: #7aada0;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-base) !important;
        color: var(--text-primary);
        font-family: 'Space Grotesk', sans-serif;
    }

    div.stButton > button {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        width: 100% !important;
        height: 110px !important;
        transition: all 0.3s ease;
        text-align: left !important;
        color: var(--text-primary) !important;
        white-space: pre-line !important;
    }

    div.stButton > button:hover {
        border-color: var(--accent-em) !important;
        transform: translateY(-3px);
        background-color: #16202a !important;
    }

    .header-wrapper {
        padding: 1.5rem;
        background: linear-gradient(135deg, #0e1a1c 0%, #101e20 100%);
        border-radius: 16px;
        border: 1px solid #2a4a44;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================
# DATA LOADING & UTILS
# =============================
C_GREEN, C_AMBER, C_RED = "#10b981", "#f59e0b", "#f43f5e"

def apply_base_layout(fig, height=500):
    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="#7aada0", size=13),
        margin=dict(l=10, r=10, t=50, b=10)
    )
    return fig

@st.cache_data
def load_data():
    # Caminho relativo — funciona local e no Streamlit Cloud
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, "DATA SET - SALES PIPELINE.zip")

    with zipfile.ZipFile(zip_path) as z:
        with z.open('sales_pipeline.csv') as f:
            df = pd.read_csv(f)

    df['engage_date'] = pd.to_datetime(df['engage_date'])
    df['close_date']  = pd.to_datetime(df['close_date'], errors='coerce')
    df['close_value'] = pd.to_numeric(df['close_value'], errors='coerce').fillna(0)
    df['status']      = df['deal_stage'].map({'Won': 'Ganho', 'Lost': 'Perdido', 'Engaging': 'Em aberto'})
    df['tempo_dias']  = (df['close_date'] - df['engage_date']).dt.days
    df['receita_real'] = df.apply(
        lambda r: r['close_value'] if r['status'] == 'Ganho' else 0, axis=1
    )
    return df

df = load_data()

# =============================
# HEADER
# =============================
st.markdown("""
<div class="header-wrapper">
    <h1 style='margin:0; font-family:Outfit;'>Sales Pipeline <span style='color:#10b981'>Performance</span></h1>
    <p style='color:#7aada0; margin:0;'>Dashboard Executivo &bull; Inteligencia Competitiva de Vendas</p>
</div>
""", unsafe_allow_html=True)

# =============================
# KPI BUTTONS
# =============================
c1, c2, c3, c4, c5 = st.columns(5)

receita_total = df['receita_real'].sum()
ganhos        = len(df[df['status'] == 'Ganho'])
perdas        = len(df[df['status'] == 'Perdido'])
conv          = (ganhos / (ganhos + perdas) * 100) if (ganhos + perdas) > 0 else 0
tm_geral      = receita_total / ganhos if ganhos > 0 else 0
ciclo_geral   = df[df['status'] == 'Ganho']['tempo_dias'].mean()

with c1:
    if st.button(f"TOTAL DEALS\n{len(df):,}"):
        st.session_state.grafico_ativo = "Deals"
with c2:
    if st.button(f"RECEITA TOTAL\nR$ {receita_total/1e6:.2f}M"):
        st.session_state.grafico_ativo = "Receita"
with c3:
    if st.button(f"CONVERSAO\n{conv:.1f}%"):
        st.session_state.grafico_ativo = "Conversao"
with c4:
    if st.button(f"TICKET MEDIO\nR$ {tm_geral:,.0f}"):
        st.session_state.grafico_ativo = "Ticket"
with c5:
    if st.button(f"CICLO MEDIO\n{ciclo_geral:.0f}d"):
        st.session_state.grafico_ativo = "Ciclo"

st.markdown("---")

# =============================
# AREA DINAMICA
# =============================

if st.session_state.grafico_ativo == "Deals":
    st.subheader("Volume e Distribuicao de Status")
    col_a, col_b = st.columns(2)

    with col_a:
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        fig_f = go.Figure(go.Funnel(
            y=status_counts['status'],
            x=status_counts['count'],
            marker_color=[C_AMBER, C_GREEN, C_RED],
            textfont=dict(size=14)
        ))
        st.plotly_chart(apply_base_layout(fig_f), width='stretch')

    with col_b:
        fig_p = px.pie(
            df, names='status', hole=0.6,
            color='status',
            color_discrete_map={'Ganho': C_GREEN, 'Perdido': C_RED, 'Em aberto': C_AMBER}
        )
        fig_p.update_traces(textfont=dict(size=13))
        st.plotly_chart(apply_base_layout(fig_p), width='stretch')

elif st.session_state.grafico_ativo == "Receita":
    st.subheader("Vendedores — Receita Real")
    rec_vend = (
        df.groupby('sales_agent')['receita_real']
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    fig_r = px.bar(
        rec_vend, x='receita_real', y='sales_agent',
        orientation='h', text_auto='.3s',
        color_discrete_sequence=[C_GREEN],
        labels={'sales_agent': 'Vendedor', 'receita_real': 'Receita'}
    )
    fig_r.update_traces(textposition='outside', cliponaxis=False, textfont=dict(size=12))
    st.plotly_chart(apply_base_layout(fig_r, height=max(500, len(rec_vend) * 30)), width='stretch')

elif st.session_state.grafico_ativo == "Conversao":
    st.subheader("Conversao por Produto")
    df_counts = df.groupby(['product', 'status']).size().reset_index(name='quantidade')
    df_total  = df.groupby('product').size().reset_index(name='total_prod')
    df_plot   = df_counts.merge(df_total, on='product')
    df_plot['percentual'] = (df_plot['quantidade'] / df_plot['total_prod'] * 100).round(1)

    fig_c = px.bar(
        df_plot, x='product', y='percentual',
        color='status', text='quantidade',
        color_discrete_map={'Ganho': C_GREEN, 'Perdido': C_RED, 'Em aberto': C_AMBER},
        category_orders={"status": ["Em aberto", "Ganho", "Perdido"]}
    )
    fig_c.update_traces(
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(size=12)
    )
    fig_c.update_layout(xaxis=dict(tickangle=-35))
    st.plotly_chart(apply_base_layout(fig_c), width='stretch')

elif st.session_state.grafico_ativo == "Ticket":
    st.subheader("Ticket Medio por Produto")
    tm_prod = (
        df[df['status'] == 'Ganho']
        .groupby('product')['close_value']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_t = px.bar(
        tm_prod, x='product', y='close_value',
        color='close_value',
        text=tm_prod['close_value'].apply(lambda x: f"R$ {x:,.0f}"),
        color_continuous_scale='Viridis',
        labels={'close_value': 'Ticket Medio'}
    )
    fig_t.update_traces(textposition='outside', textfont=dict(size=12))
    fig_t.update_layout(coloraxis_showscale=False, xaxis=dict(tickangle=-35))
    st.plotly_chart(apply_base_layout(fig_t), width='stretch')

elif st.session_state.grafico_ativo == "Ciclo":
    st.subheader("Tendencia: Ciclo de Fechamento")
    df_trend = df[df['status'] == 'Ganho'].copy().sort_values('close_date')

    fig_s = px.scatter(
        df_trend,
        x='close_date', y='tempo_dias',
        color='product',
        trendline="ols",
        labels={
            'close_date': 'Data de Fechamento',
            'tempo_dias': 'Ciclo (Dias)',
            'product': 'Produto'
        },
        hover_data=['sales_agent', 'close_value'],
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_s.update_traces(marker=dict(size=9, opacity=0.7))
    st.plotly_chart(apply_base_layout(fig_s, height=600), width='stretch')