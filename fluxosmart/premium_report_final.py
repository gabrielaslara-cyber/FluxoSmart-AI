"""ReportLab-only premium management report."""
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.graphics.shapes import Drawing,Rect,String
from fluxosmart.analytics import summarize_sales
from fluxosmart.diagnostics import diagnose_sales

def money(n):
    return ("R$ {:,.2f}".format(n)).replace(",","X").replace(".",",").replace("X",".")

def chart(series,title):
    d=Drawing(475,170)
    d.add(String(4,149,title,fontSize=11,fontName="Helvetica-Bold"))
    if not series.empty:
        scale=max(float(series.max()),1)
        for i,(key,val) in enumerate(series.head(5).items()):
            y=120-i*24
            d.add(String(4,y+2,str(key)[:24],fontSize=8))
            d.add(Rect(158,y,205*float(val)/scale,11,fillColor=colors.HexColor("#15956e"),strokeColor=None))
            d.add(String(370,y+2,money(float(val)),fontSize=8))
    return d

def build_sales_report(df):
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,leftMargin=44,rightMargin=44,topMargin=45,bottomMargin=45)
    s=getSampleStyleSheet()
    s["Title"].fontSize=19
    s["Title"].leading=24
    s["Title"].textColor=colors.HexColor("#123c33")
    s["Heading2"].textColor=colors.HexColor("#176c55")
    issued=datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y às %H:%M")
    story=[Paragraph("FluxoSmart AI | Relatório Premium",s["Title"]),
           Paragraph("Relatório demonstrativo; diagnósticos por regras, sem IA generativa.",s["Normal"]),
           Paragraph(f"Emitido em: {issued} (horário de Brasília)",s["Normal"]),Spacer(1,15)]
    if df.empty:
        story.append(Paragraph("Nenhum registro com os filtros escolhidos.",s["Normal"]))
    else:
        m=summarize_sales(df)
        start=df["data"].min().strftime("%d/%m/%Y")
        end=df["data"].max().strftime("%d/%m/%Y")
        story.append(Paragraph(f"Período: {start} a {end}",s["Heading3"]))
        items=[["Indicador","Valor"],["Faturamento",money(m["faturamento"])],
            ["Unidades vendidas",f'{m["unidades"]:g}'],["Pedidos" if m["base_ticket"] == "pedido" else "Registros",str(m["registros"])],
            ["Ticket médio",money(m["ticket_medio"])]]
        table=Table(items,colWidths=[280,190])
        table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#d9f2e7")),
        ("GRID",(0,0),(-1,-1),.4,colors.grey),("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)]))
        story.extend([table,Spacer(1,18),
            chart(df.groupby("categoria")["faturamento"].sum().sort_values(ascending=False),"Faturamento por categoria"),
            chart(df.groupby("produto")["faturamento"].sum().sort_values(ascending=False),"Faturamento por produto"),
            Paragraph("Barras proporcionais ao faturamento de cada categoria ou produto no período. Valores em reais; isto não representa lucro.",s["Normal"]),
            PageBreak(),Paragraph("Diagnósticos e plano de ação",s["Title"])])
        for item in diagnose_sales(df):
            story.extend([Paragraph(str(item["titulo"]),s["Heading3"]),
                          Paragraph(re.sub(r"(-?\\d+)\\.(\\d+)%",r"\\1,\\2%",str(item["descricao"])),s["BodyText"]),Spacer(1,8)])
        story.append(Paragraph("Recomendações para investigação",s["Heading2"]))
        for line in ["Conferir estoque e margem dos produtos líderes.",
                     "Comparar períodos e verificar fatores que influenciam a demanda.",
                     "Incluir custos e descontos antes de avaliar rentabilidade."]:
            story.append(Paragraph("• "+line,s["BodyText"]))
        story.extend([Spacer(1,20),Paragraph("Limites: faturamento não equivale a lucro. Os resultados não são previsões. Use somente dados fictícios ou autorizados.",s["BodyText"])])
    doc.build(story)
    return buf.getvalue()
