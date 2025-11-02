import requests
from bs4 import BeautifulSoup

def fetch_yahoo_tw():
    url = "https://tw.stock.yahoo.com/news"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    news = []
    for a in soup.select("a[href*='/news/']")[:8]:
        title = a.get_text().strip()
        href = a.get('href', '')
        if not href:
            continue
        link = "https://tw.stock.yahoo.com" + href if href.startswith('/') else href
        news.append({'market': '台股', 'source': 'Yahoo奇摩', 'title': title, 'url': link})
    return news

def fetch_cnyes():
    url = "https://news.cnyes.com/news/cat/tw_stock"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    news = []
    for a in soup.select("a[href*='/news/id/']")[:8]:
        title = a.get_text().strip()
        href = a.get('href', '')
        link = "https://news.cnyes.com" + href if href.startswith('/') else href
        news.append({'market': '台股', 'source': '鉅亨網', 'title': title, 'url': link})
    return news

def fetch_cna():
    url = "https://www.cna.com.tw/list/aall.aspx"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    news = []
    for a in soup.select("a[href*='/news/']")[:8]:
        title = a.get_text().strip()
        href = a.get('href', '')
        link = "https://www.cna.com.tw" + href if href.startswith('/') else href
        news.append({'market': '台股', 'source': '中央社', 'title': title, 'url': link})
    return news

def fetch_cnbc():
    url = "https://www.cnbc.com/world/?region=world"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    news = []
    # CNBC 正式網站標題選取可能變動，這裡嘗試常見選擇器
    for a in soup.select("a.Card-title")[:8]:
        title = a.get_text().strip()
        href = a.get('href', '')
        link = href if href.startswith('http') else "https://www.cnbc.com" + href
        news.append({'market': '美股', 'source': 'CNBC', 'title': title, 'url': link})
    return news

def fetch_marketwatch():
    url = "https://www.marketwatch.com/latest-news"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    news = []
    for a in soup.select("a.article__headline")[:8]:
        title = a.get_text().strip()
        href = a.get('href', '')
        link = href if href.startswith('http') else "https://www.marketwatch.com" + href
        news.append({'market': '美股', 'source': 'MarketWatch', 'title': title, 'url': link})
    return news

def get_all_news():
    all_news = []
    for func in (fetch_yahoo_tw, fetch_cnyes, fetch_cna, fetch_cnbc, fetch_marketwatch):
        try:
            all_news.extend(func())
        except Exception as e:
            print(f'fetch error {func.__name__}:', e)
    # 去重標題並保留順序
    seen = set()
    unique = []
    for n in all_news:
        t = n.get('title','')
        if t and t not in seen:
            seen.add(t)
            unique.append(n)
    return unique[:20]
