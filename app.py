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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family:'Inter',sans-serif}
[data-testid="stAppViewContainer"] {background: #f5f8f7}
.block-container {padding-top:2.3rem; padding-bottom:4rem; max-width:1480px}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#0e2928,#102c2b 65%,#163e37)!important}
[data-testid="stSidebar"] * {color:#eafcf7!important}
[data-testid="stSidebar"] label {color:#e5f8f0!important}
[data-testid="stSidebar"] [data-baseweb="select"] * {color:#1a3330!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {border-radius:12px}
.hero {padding:36px 39px; border-radius:24px; background:linear-gradient(110deg,#0b2929 0%,#145e50 60%,#20a57b 100%); box-shadow:0 12px 32px rgba(10,55,47,.13);margin:0 0 24px; position:relative;overflow:hidden}
.hero:after {content:"";position:absolute;width:300px;height:300px;right:-70px;top:-170px;background:rgba(147,255,207,.08);border:2px solid rgba(193,255,222,.14);border-radius:50%}
.hero .eyebrow {font-size:.74rem;letter-spacing:.18em;font-weight:800;color:#97f5c7;margin-bottom:12px}
.hero h1 {font-size:2.45rem;line-height:1.1;color:#fff!important;margin:0;font-weight:800;letter-spacing:-.04em}
.hero p {font-size:1rem;color:#c8f0e3!important;margin:14px 0 0}
.pill {display:inline-block;margin-top:20px;padding:7px 14px;border-radius:100px;background:rgba(161,255,206,.13);border:1px solid rgba(184,255,221,.28);font-size:.78rem;color:#d4ffe7;font-weight:600}
[data-testid="stMetric"] {background:#fff;border:1px solid #e1ece8;border-radius:20px;padding:22px 22px 20px;box-shadow:0 4px 15px rgba(28,69,57,.045);min-height:136px}
[data-testid="stMetricLabel"] {color:#74847d!important;font-size:.86rem}
[data-testid="stMetricValue"] {color:#173a31!important;font-size:1.8rem;font-weight:800}
[data-testid="stMetric"]::before {content:"";display:block;width:30px;height:4px;border-radius:5px;background:#28c68c;margin-bottom:12px}
[data-testid="stTabs"] [data-baseweb="tab-list"] {gap:8px;padding:8px;background:#e9f1ee;border-radius:14px}
[data-testid="stTabs"] [data-baseweb="tab"] {border-radius:10px;padding:12px 19px;font-weight:600;color:#536e63}
[data-testid="stTabs"] [aria-selected="true"] {background:#fff!important;color:#0a8061!important;box-shadow:0 2px 9px rgba(10,58,45,.08)}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {background:transparent}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:16px}
[data-testid="stDataFrame"] {border-radius:14px;overflow:hidden}
.stDownloadButton button {background:#0f8769!important;color:white!important;border:0!important;border-radius:12px!important;font-weight:700;padding:12px 20px}
.stDownloadButton button:hover {background:#08684f!important}
h2,h3 {color:#1b4238!important;letter-spacing:-.02em}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="eyebrow">● BUSINESS INTELLIGENCE • 2.0</div><h1>FluxoSmart AI <span style="color:#8ef0bc">↗</span></h1><p>Transforme planilhas em decisões inteligentes para seu negócio.</p><span class="pill">✦ Painel demonstrativo · Análise de vendas</span></div>', unsafe_allow_html=True)
st.caption("Demonstração com dados fictícios. Diagnósticos baseados em regras, sem IA generativa.")

with st.sidebar:
    st.title("◈ FluxoSmart")
    st.caption("WORKSPACE / ANALYTICS")
    st.markdown("### ⚙️ Controle do painel")
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
