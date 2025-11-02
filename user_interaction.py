from linebot.models import TextSendMessage
from news_scraper import get_all_news

def build_reply_for_query(query):
    q = query.lower()
    all_news = get_all_news()
    if '台股' in q:
        filtered = [n for n in all_news if n.get('market') == '台股'][:8]
    elif '美股' in q:
        filtered = [n for n in all_news if n.get('market') == '美股'][:8]
    else:
        filtered = all_news[:8]
    lines = []
    for n in filtered:
        lines.append(f"🌐 {n.get('market')}｜{n.get('source')}\n{n.get('title')}\n🔗 {n.get('url')}")
    return "\n\n".join(lines) if lines else '找不到相關新聞'
