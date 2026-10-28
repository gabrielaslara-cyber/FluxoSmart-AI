import pandas as pd
from fluxosmart.analytics import prepare_sales
from fluxosmart.reports import build_sales_report

def test_pdf_report_with_sales():
    df = prepare_sales(pd.DataFrame({"data":["2026-01-01"],"produto":["Café"],"categoria":["Alimentos"],"quantidade":[2],"preco_unitario":[10]}))
    pdf = build_sales_report(df)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000

def test_pdf_report_empty():
    df = prepare_sales(pd.DataFrame(columns=["data","produto","categoria","quantidade","preco_unitario"]))
    assert build_sales_report(df).startswith(b"%PDF")
