"""FluxoSmart AI 2.0 — painel demonstrativo de vendas."""
from pathlib import Path
import pandas as pd
import streamlit as st
from fluxosmart.analytics import prepare_sales, summarize_sales
from fluxosmart.diagnostics import diagnose_sales
from fluxosmart.reports import build_sales_report

st.set_page_config(page_title="FluxoSmart AI | Gestão inteligente", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1450px}
[data-testid="stMetric"] {background: #f1f7fa; border: 1px solid #dce9ee; border-radius: 14px; padding: 16px 18px}
[data-testid="stMetricLabel"] {color:#496272}
[data-testid="stMetricValue"] {color:#102f42; font-weight:700}
.hero {padding:24px 28px; border-radius:20px; background:linear-gradient(115deg,#103b53,#087f80); color:white; margin-bottom:20px}
.hero h1 {color:white!important; margin:0; font-size:2.1rem}
.hero p {color:#d9f5f3!important; margin:8px 0 0}
.small-note {color:#64748b; font-size:.9rem}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📊 FluxoSmart AI</h1><p>Inteligência de vendas para pequenos negócios · Dashboard 2.0</p></div>', unsafe_allow_html=True)
st.caption("Demonstração com dados fictícios. Diagnósticos baseados em regras, sem IA generativa.")

with st.sidebar:
    st.title("⚙️ Painel de controle")
    st.markdown("**Fonte dos dados**")
    upload = st.file_uploader("Envie Excel ou CSV", type=["xlsx", "csv"])
    st.caption("Não envie informações pessoais ou sigilosas para esta demonstração pública.")

try:
    if upload is None:
        source = Path(__file__).parent / "data" / "vendas_exemplo.csv"
        raw = pd.read_csv(source)
        source_name = "Dados fictícios de demonstração"
    elif upload.name.lower().endswith(".csv"):
        raw = pd.read_csv(upload)
        source_name = upload.name
    else:
        raw = pd.read_excel(upload)
        source_name = upload.name
    df = prepare_sales(raw)
except (ValueError, KeyError, OSError, ImportError, pd.errors.ParserError) as exc:
    st.error(f"Não foi possível processar a planilha: {exc}")
    st.stop()

with st.sidebar:
    st.divider()
    st.markdown("**Filtros**")
    categories = sorted(df["categoria"].dropna().astype(str).unique().tolist())
    selected = st.multiselect("Categorias", categories, default=categories)
    if not df.empty:
        min_date = df["data"].min().date()
        max_date = df["data"].max().date()
        dates = st.date_input("Período", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    else:
        dates = ()
    st.divider()
    st.caption("FluxoSmart AI 2.0 · Portfólio de Gabriela de Souza Lara")

filtered = df[df["categoria"].astype(str).isin(selected)].copy()
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    filtered = filtered[filtered["data"].dt.date.between(dates[0], dates[1])]

def brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

metrics = summarize_sales(filtered)
st.markdown(f"**Fonte:** {source_name} &nbsp; | &nbsp; **Registros após filtros:** {len(filtered)}")
a, b, c, d = st.columns(4)
a.metric("Faturamento", brl(metrics["faturamento"]))
b.metric("Unidades vendidas", f'{metrics["unidades"]:,.0f}'.replace(",", "."))
c.metric("Pedidos" if metrics["base_ticket"] == "pedido" else "Registros", metrics["registros"])
d.metric("Ticket médio", brl(metrics["ticket_medio"]), help=f'Calculado por {metrics["base_ticket"]}.')

tab_dashboard, tab_diagnostico, tab_relatorios, tab_dados = st.tabs(
    ["📈 Visão geral", "🔎 Diagnósticos", "📄 Relatórios", "🗂️ Dados"]
)

with tab_dashboard:
    if filtered.empty:
        st.info("Nenhuma venda encontrada para os filtros selecionados.")
    else:
        left, right = st.columns([1.3, 1])
        with left:
            st.subheader("Evolução do faturamento")
            daily = filtered.groupby(filtered["data"].dt.date)["faturamento"].sum().sort_index()
            st.line_chart(daily, x_label="Data", y_label="Faturamento (R$)")
        with right:
            st.subheader("Faturamento por categoria")
            by_cat = filtered.groupby("categoria")["faturamento"].sum().sort_values(ascending=False)
            st.bar_chart(by_cat, x_label="Categoria", y_label="Faturamento (R$)")
        st.subheader("Produtos com maior faturamento")
        ranking = (filtered.groupby("produto", as_index=False)
                   .agg(unidades=("quantidade", "sum"), faturamento=("faturamento", "sum"))
                   .sort_values("faturamento", ascending=False).head(10))
        st.dataframe(ranking, use_container_width=True, hide_index=True)

with tab_diagnostico:
    st.subheader("Diagnóstico automático")
    st.caption("Observações descritivas geradas por regras. Elas não substituem análise de custos, margens, estoque e sazonalidade.")
    for insight in diagnose_sales(filtered):
        message = f'**{insight["titulo"]}** — {insight["descricao"]}'
        if insight["nivel"] == "atencao":
            st.warning(message)
        else:
            st.info(message)

with tab_relatorios:
    st.subheader("Exportação de relatórios")
    st.write("Os arquivos consideram apenas os registros incluídos nos filtros.")
    st.download_button(
        "📄 Baixar relatório gerencial em PDF",
        data=build_sales_report(filtered),
        file_name="fluxosmart_relatorio_gerencial.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.download_button(
        "📥 Baixar dados filtrados em CSV",
        data=filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="fluxosmart_vendas_filtradas.csv",
        mime="text/csv",
        use_container_width=True,
    )

with tab_dados:
    st.subheader("Dados processados")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    with st.expander("Formato de planilha aceito"):
        st.write("Colunas obrigatórias: data, produto, categoria, quantidade, preco_unitario.")
        st.write("Coluna opcional: pedido_id (permite cálculo do ticket médio por pedido).")
        st.info("Faturamento = quantidade × preço unitário. Descontos, impostos e devoluções não são considerados.")
