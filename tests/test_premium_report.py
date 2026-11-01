from io import BytesIO
import pandas as pd
from pypdf import PdfReader
from fluxosmart.analytics import prepare_sales
from fluxosmart.premium_report_v2 import build_sales_report

def test_premium_pdf_with_sales():
    df = prepare_sales(pd.DataFrame({
        "data":["2026-01-01","2026-01-02"],
        "produto":["Caneta","Caderno"],
        "categoria":["Papelaria","Papelaria"],
        "quantidade":[2,3],
        "preco_unitario":[5,12]
    }))
    result = build_sales_report(df)
    assert result.startswith(b"%PDF")
    assert len(PdfReader(BytesIO(result)).pages) >= 2

def test_premium_pdf_empty():
    df = prepare_sales(pd.DataFrame({
        "data":["2026-01-01"],"produto":["Caneta"],
        "categoria":["Papelaria"],"quantidade":[2],"preco_unitario":[5]
    })).iloc[0:0]
    assert build_sales_report(df).startswith(b"%PDF")
