"""Premium charts, appended to the standard ReportLab PDF."""
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from fluxosmart.reports import build_sales_report as original

def build_sales_report(df):
    base = PdfReader(BytesIO(original(df)))
    if df.empty:
        return BytesIO(original(df)).getvalue()
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 17)
    c.drawString(50, h-65, "FluxoSmart AI | Analise de faturamento")
    for title, group, y0 in [
        ("Categorias", df.groupby("categoria")["faturamento"].sum().sort_values(ascending=False), h-115),
        ("Produtos", df.groupby("produto")["faturamento"].sum().sort_values(ascending=False), h-355)
    ]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50,y0,title)
        top = max(float(group.max()),1)
        for i,(name,value) in enumerate(group.head(5).items()):
            y = y0-30-i*32
            c.setFont("Helvetica",9)
            c.drawString(50,y,str(name)[:24])
            c.setFillColorRGB(.07,.52,.39)
            c.rect(195,y-2,210*float(value)/top,12,fill=1,stroke=0)
            c.setFillColorRGB(0,0,0)
            c.drawString(414,y,f"R$ {float(value):.2f}")
    c.setFont("Helvetica",9)
    c.drawString(50,95,"Acoes: conferir margens e estoque; investigar variacoes; monitorar custos.")
    c.drawString(50,75,"Resultados descritivos. Nao representam previsoes nem lucro.")
    c.showPage()
    c.save()
    writer=PdfWriter()
    writer.append_pages_from_reader(base)
    writer.append_pages_from_reader(PdfReader(BytesIO(buf.getvalue())))
    output=BytesIO()
    writer.write(output)
    return output.getvalue()
