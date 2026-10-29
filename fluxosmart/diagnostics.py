"""Deterministic, explainable sales diagnostics. No external API required."""
from __future__ import annotations
import pandas as pd

def diagnose_sales(df: pd.DataFrame) -> list[dict[str, str]]:
    """Return grounded insights from already filtered and validated sales rows."""
    if df.empty:
        return [{"nivel": "info", "titulo": "Sem vendas no filtro", "descricao": "Amplie o período ou selecione outras categorias."}]
    insights = []
    total = float(df["faturamento"].sum())
    categories = df.groupby("categoria", dropna=False)["faturamento"].sum().sort_values(ascending=False)
    if total > 0 and not categories.empty:
        top_name = str(categories.index[0])
        share = float(categories.iloc[0] / total * 100)
        insights.append({"nivel": "info", "titulo": "Categoria líder", "descricao": f"{top_name} representa {share:.1f}% do faturamento no período filtrado."})
        if share >= 60:
            insights.append({"nivel": "atencao", "titulo": "Concentração de vendas", "descricao": f"{share:.1f}% do faturamento está em uma categoria. Avalie a diversificação, considerando a demanda e as margens."})
    products = df.groupby("produto", dropna=False)["quantidade"].sum().sort_values(ascending=False)
    if not products.empty:
        insights.append({"nivel": "info", "titulo": "Produto mais vendido", "descricao": f"{products.index[0]} lidera em unidades ({products.iloc[0]:g}) no período selecionado."})
    daily = df.groupby(df["data"].dt.normalize())["faturamento"].sum().sort_index()
    if len(daily) >= 4:
        midpoint = len(daily) // 2
        first = float(daily.iloc[:midpoint].mean())
        second = float(daily.iloc[midpoint:].mean())
        if first > 0:
            change = (second / first - 1) * 100
            insights.append({"nivel": "atencao" if change < -10 else "info", "titulo": "Evolução entre dias com vendas", "descricao": f"A média de faturamento por dia com vendas variou {change:+.1f}% entre as duas metades dos dias registrados. Dias sem vendas não são incluídos; isso não indica tendência causal."})
    return insights
