"""Streamlit dashboard for sales analytics."""
from pathlib import Path
import pandas as pd
import streamlit as st
from fluxosmart.analytics import prepare_sales, summarize_sales

st.set_page_config(page_title="FluxoSmart AI | Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f5f7fb; }
.block-container { padding-top: 2.3rem; padding-bottom: 3rem; max-width: 1450px; }
h1,h2,h3 { color: #10213a; letter-spacing: -.025em; }
[data-testid="stMetric"] { background: white; border: 1px solid #e2e8f0; padding: 1.1rem 1.2rem; border-radius: 16px; box-shadow: 0 5px 16px #10213a09; }
[data-testid="stMetricLabel"] { font-size: .91rem; color: #52647c; }
[data-testid="stMetricValue"] { color: #0e7490; }
[data-testid="stSidebar"] { background: #eaf1f8; }
</style>
""", unsafe_allow_html=True)
st.title("FluxoSmart AI")
st.caption("Inteligência de vendas • Painel demonstrativo 2.0")
st.info("Demonstração com dados fictícios. O projeto ainda não utiliza IA generativa.")

with st.sidebar:
    st.header("Filtros e dados")
    upload = st.file_uploader("Importar planilha (.xlsx ou .csv)", type=["xlsx", "csv"])
    st.caption("Use suas próprias planilhas ou explore os dados fictícios.")
try:
    if upload is None:
        source = Path(__file__).parent / "data" / "vendas_exemplo.csv"
        raw = pd.read_csv(source)
        st.caption("Exibindo dados fictícios de demonstração.")
    elif upload.name.lower().endswith(".csv"):
        raw = pd.read_csv(upload)
    else:
        raw = pd.read_excel(upload)
    df = prepare_sales(raw)
except (ValueError, KeyError, OSError, ImportError) as exc:
    st.error(f"Não foi possível ler os dados: {exc}")
    st.stop()

categories = sorted(df["categoria"].dropna().astype(str).unique().tolist())
with st.sidebar:
    selected = st.multiselect("Categorias", categories, default=categories)
filtered = df[df["categoria"].astype(str).isin(selected)]
if not filtered.empty:
    min_date = filtered["data"].min().date()
    max_date = filtered["data"].max().date()
    with st.sidebar:
        dates = st.date_input("Intervalo de datas", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(dates, (tuple, list)) and len(dates) == 2:
        filtered = filtered[filtered["data"].dt.date.between(dates[0], dates[1])]

st.subheader("Visão geral")
metrics = summarize_sales(filtered)
fmt = lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
a, b, c, d = st.columns(4)
a.metric("Faturamento", fmt(metrics["faturamento"]))
b.metric("Unidades vendidas", f"{metrics['unidades']:,.0f}")
c.metric("Pedidos" if metrics["base_ticket"] == "pedido" else "Registros", metrics["registros"])
d.metric(f"Ticket médio por {metrics['base_ticket']}", fmt(metrics["ticket_medio"]))
left, right = st.columns(2)
with left:
    st.subheader("Faturamento por dia")
    daily = filtered.groupby(filtered["data"].dt.date)["faturamento"].sum().sort_index()
    st.line_chart(daily)
with right:
    st.subheader("Faturamento por categoria")
    by_cat = filtered.groupby("categoria")["faturamento"].sum().sort_values(ascending=False)
    st.bar_chart(by_cat)
st.subheader("Dados filtrados")
st.dataframe(filtered, use_container_width=True)
st.download_button("Exportar dados filtrados (CSV)", data=filtered.to_csv(index=False).encode("utf-8-sig"),
                   file_name="fluxosmart_vendas_filtradas.csv", mime="text/csv")
