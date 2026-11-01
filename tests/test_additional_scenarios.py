import pandas as pd
import pytest
from fluxosmart.analytics import prepare_sales, summarize_sales
from fluxosmart.diagnostics import diagnose_sales

def sample():
    return pd.DataFrame({
        "data":["2026-01-01","2026-01-02","2026-01-03","2026-01-04"],
        "produto":["Café","Chá","Caneta","Caderno"],
        "categoria":["Alimentos","Alimentos","Papelaria","Papelaria"],
        "quantidade":[1,2,3,4],"preco_unitario":[10,12,2,15],
        "pedido_id":["A","B","C","D"]})

def test_csv_roundtrip():
    from io import StringIO
    raw=sample()
    data=pd.read_csv(StringIO(raw.to_csv(index=False)))
    assert summarize_sales(prepare_sales(data))["faturamento"] == 100

def test_xlsx_roundtrip(tmp_path):
    p=tmp_path/"vendas.xlsx"
    sample().to_excel(p,index=False)
    data=pd.read_excel(p)
    assert summarize_sales(prepare_sales(data))["registros"] == 4

@pytest.mark.parametrize("column",["data","quantidade","preco_unitario"])
def test_invalid_values(column):
    df=sample()
    df.loc[0,column]="invalido"
    with pytest.raises(ValueError):
        prepare_sales(df)

def test_no_orders_uses_row_count():
    df=prepare_sales(sample().drop(columns=["pedido_id"]))
    assert summarize_sales(df)["base_ticket"] == "registro"

def test_empty_diagnostics():
    df=prepare_sales(sample()).iloc[:0]
    assert diagnose_sales(df)[0]["titulo"] == "Sem vendas no filtro"

def test_zero_revenue_handled():
    df=sample()
    df["preco_unitario"]=0
    result=prepare_sales(df)
    assert summarize_sales(result)["faturamento"] == 0

def test_negative_price_rejected():
    df=sample()
    df.loc[0,"preco_unitario"]=-1
    with pytest.raises(ValueError):
        prepare_sales(df)
