import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from news_scraper import get_all_news
from trend_analyzer import analyze_trend
from summary_helper import summarize_title
from report_generator import generate_daily_report

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
USER_ID = os.getenv('USER_ID')

if not LINE_CHANNEL_ACCESS_TOKEN or not USER_ID:
    print('請先在環境變數設定 LINE_CHANNEL_ACCESS_TOKEN 與 USER_ID')
else:
    line_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

    def send_text(msg):
        try:
            line_api.push_message(USER_ID, TextSendMessage(text=msg))
        except Exception as e:
            print('LINE push error:', e)

    def run_push():
        news = get_all_news()
        enriched = []
        if not news:
            send_text('今天暫無最新股市新聞。')
            return
        send_text('📢 今日台股 & 美股 最新新聞摘要：')
        for n in news:
            title = n.get('title','')
            summary = summarize_title(title)
            trend = analyze_trend(title + '\n' + summary)
            n['summary'] = summary
            n['trend'] = trend
            enriched.append(n)
            msg = f"🌐 {n.get('market')}｜{n.get('source')}\n{title}\n🧠 摘要：{summary}\n📊 趨勢判斷：{trend}\n🔗 {n.get('url')}"]
            send_text(msg)
        # 產生報告檔案（可選）
        try:
            pdf = generate_daily_report(enriched)
            print('報告已建立：', pdf)
        except Exception as e:
            print('產生報告失敗：', e)

    if __name__ == '__main__':
        run_push()
