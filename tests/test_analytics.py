import pandas as pd
import pytest
from fluxosmart.analytics import prepare_sales, summarize_sales

def example():
    return pd.DataFrame({"data": ["2026-01-01", "2026-01-02"], "produto": ["A", "B"],
                         "categoria": ["X", "Y"], "quantidade": [2, 1], "preco_unitario": [10, 30]})

def test_revenue_and_metrics():
    result = prepare_sales(example())
    assert result["faturamento"].tolist() == [20, 30]
    summary = summarize_sales(result)
    assert summary["faturamento"] == 50
    assert summary["ticket_medio"] == 25

def test_missing_column():
    with pytest.raises(ValueError, match="Colunas obrigatórias"):
        prepare_sales(example().drop(columns=["categoria"]))

def test_negative_quantity():
    bad = example()
    bad.loc[0, "quantidade"] = -1
    with pytest.raises(ValueError, match="Quantidades"):
        prepare_sales(bad)

def test_order_ticket_uses_distinct_orders():
    raw = example().assign(pedido_id=["ABC", "ABC"])
    metrics = summarize_sales(prepare_sales(raw))
    assert metrics["registros"] == 1
    assert metrics["ticket_medio"] == 50

def test_empty_summary():
    assert summarize_sales(prepare_sales(example()).iloc[0:0])["faturamento"] == 0
