"""PDF report from filtered sales data; no external services."""
from __future__ import annotations
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from fluxosmart.analytics import summarize_sales
from fluxosmart.diagnostics import diagnose_sales

def build_sales_report(df) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(21*cm, 29.7*cm), rightMargin=1.8*cm, leftMargin=1.8*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=19, textColor=colors.HexColor("#15364B"), spaceAfter=12))
    styles.add(ParagraphStyle(name="ReportBody", parent=styles["BodyText"], fontSize=10, leading=15, spaceAfter=8))
    styles.add(ParagraphStyle(name="ReportSmall", parent=styles["BodyText"], fontSize=8, leading=12, textColor=colors.grey))
    story = [Paragraph("FluxoSmart AI | Relatório gerencial", styles["ReportTitle"]),
             Paragraph("Análise automática baseada nos dados selecionados. Sem IA generativa.", styles["ReportSmall"]), Spacer(1, 12)]
    if df.empty:
        story.append(Paragraph("Não há vendas no período e nas categorias selecionados.", styles["ReportBody"]))
    else:
        start, end = df["data"].min().strftime("%d/%m/%Y"), df["data"].max().strftime("%d/%m/%Y")
        story.append(Paragraph(f"Período dos registros: {start} a {end}", styles["ReportBody"]))
        metrics = summarize_sales(df)
        money = lambda x: ("R$ {:,.2f}".format(x)).replace(",", "X").replace(".", ",").replace("X", ".")
        rows = [["Indicador", "Valor"], ["Faturamento", money(metrics["faturamento"])],
                ["Unidades vendidas", f'{metrics["unidades"]:g}'],
                ["Pedidos" if metrics["base_ticket"] == "pedido" else "Registros", str(metrics["registros"])],
                ["Ticket médio por " + metrics["base_ticket"], money(metrics["ticket_medio"])]]
        table = Table(rows, colWidths=[9*cm, 7*cm], hAlign="LEFT")
        table.setStyle(TableStyle([("BACKGROUND", (0,0),(-1,0),colors.HexColor("#E6F1F8")),
                                  ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#CBD5E1")),
                                  ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),8),
                                  ("BOTTOMPADDING",(0,0),(-1,-1),8)]))
        story.extend([table, Spacer(1, 18), Paragraph("Diagnósticos e pontos de atenção", styles["Heading2"])])
        for item in diagnose_sales(df):
            story.append(KeepTogether([Paragraph(escape(item["titulo"]), styles["Heading3"]),
                                        Paragraph(escape(item["descricao"]), styles["ReportBody"])]))
    story.extend([Spacer(1, 14), Paragraph("Observações: resultados descritivos, não previsões. Considere custos, margens, estoque e sazonalidade antes de tomar decisões. Não inclua dados pessoais sensíveis nas planilhas.", styles["ReportSmall"])])
    doc.build(story)
    return buffer.getvalue()
