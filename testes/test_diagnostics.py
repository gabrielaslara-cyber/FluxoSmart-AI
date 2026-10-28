import pandas as pd
from fluxosmart.analytics import prepare_sales
from fluxosmart.diagnostics import diagnose_sales

def test_empty_sales():
    df = prepare_sales(pd.DataFrame(columns=["data", "produto", "categoria", "quantidade", "preco_unitario"]))
    assert diagnose_sales(df)[0]["titulo"] == "Sem vendas no filtro"

def test_top_category_and_product():
    raw = pd.DataFrame({
        "data": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "produto": ["Arroz", "Arroz", "Lápis", "Arroz"],
        "categoria": ["Alimentos", "Alimentos", "Papelaria", "Alimentos"],
        "quantidade": [3, 2, 1, 4],
        "preco_unitario": [10, 10, 5, 10],
    })
    insights = diagnose_sales(prepare_sales(raw))
    titles = [item["titulo"] for item in insights]
    assert "Categoria líder" in titles
    assert "Produto mais vendido" in titles
    assert "Concentração de vendas" in titles
    assert "Evolução entre dias com vendas" in titles
