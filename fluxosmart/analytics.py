"""Pure analytics functions, independent of the Streamlit UI."""
from __future__ import annotations
import pandas as pd
REQUIRED = {"data", "produto", "categoria", "quantidade", "preco_unitario"}

def prepare_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Validate a sales table and calculate revenue per line."""
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError("Colunas obrigatórias ausentes: " + ", ".join(sorted(missing)))
    out = df.copy()
    out["data"] = pd.to_datetime(out["data"], errors="coerce")
    for name in ["quantidade", "preco_unitario"]:
        out[name] = pd.to_numeric(out[name], errors="coerce")
    if out[["data", "quantidade", "preco_unitario"]].isna().any().any():
        raise ValueError("Há datas, quantidades ou preços inválidos na planilha.")
    if (out["quantidade"] <= 0).any() or (out["preco_unitario"] < 0).any():
        raise ValueError("Quantidades devem ser positivas e preços não podem ser negativos.")
    out["faturamento"] = out["quantidade"] * out["preco_unitario"]
    return out

def summarize_sales(df: pd.DataFrame) -> dict:
    """Calculate metrics; ticket per order if pedido_id exists, otherwise per row."""
    if df.empty:
        return {"faturamento": 0.0, "unidades": 0.0, "registros": 0, "ticket_medio": 0.0, "base_ticket": "registro"}
    revenue = float(df["faturamento"].sum())
    has_orders = "pedido_id" in df.columns and df["pedido_id"].notna().all()
    n = int(df["pedido_id"].nunique()) if has_orders else len(df)
    return {"faturamento": revenue, "unidades": float(df["quantidade"].sum()), "registros": n,
            "ticket_medio": revenue / n if n else 0.0, "base_ticket": "pedido" if has_orders else "registro"}
