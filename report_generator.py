from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_daily_report(news_list, filename='daily_report.pdf'):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph('📊 每日股市新聞報告', styles['Title']))
    for n in news_list:
        content.append(Spacer(1,12))
        content.append(Paragraph(f"{n.get('market','')} | {n.get('source','')} - {n.get('title','')}", styles['Heading3']))
        summary = n.get('summary','（無摘要）')
        trend = n.get('trend','⚖️ 中性')
        content.append(Paragraph(f"摘要：{summary}", styles['BodyText']))
        content.append(Paragraph(f"趨勢：{trend}", styles['BodyText']))
    doc.build(content)
    return filename
