"""Streamlit dashboard for sales analytics."""
from pathlib import Path
import pandas as pd
import streamlit as st
from fluxosmart.analytics import prepare_sales, summarize_sales
from fluxosmart.diagnostics import diagnose_sales

st.set_page_config(page_title="FluxoSmart AI", page_icon="📊", layout="wide")
st.title("📊 FluxoSmart AI")
st.caption("Painel de vendas para pequenos negócios • MVP demonstrativo")
st.info("Os dados de demonstração são fictícios. Esta versão não utiliza IA generativa.")

upload = st.file_uploader("Envie sua planilha de vendas (.xlsx ou .csv)", type=["xlsx", "csv"])
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
selected = st.multiselect("Categorias", categories, default=categories)
filtered = df[df["categoria"].astype(str).isin(selected)]
if not filtered.empty:
    min_date = filtered["data"].min().date()
    max_date = filtered["data"].max().date()
    dates = st.date_input("Intervalo de datas", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(dates, (tuple, list)) and len(dates) == 2:
        filtered = filtered[filtered["data"].dt.date.between(dates[0], dates[1])]

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
st.subheader("🔎 Diagnóstico automático de vendas")
st.caption("Análises explicáveis sem IA generativa nem custos de API. Considere margens, estoque e sazonalidade antes de agir.")
for insight in diagnose_sales(filtered):
    message = "**{}** — {}".format(insight["titulo"], insight["descricao"])
    if insight["nivel"] == "atencao":
        st.warning(message)
    else:
        st.info(message)
st.subheader("Dados filtrados")
st.dataframe(filtered, use_container_width=True)
st.download_button("Exportar dados filtrados (CSV)", data=filtered.to_csv(index=False).encode("utf-8-sig"),
                   file_name="fluxosmart_vendas_filtradas.csv", mime="text/csv")
