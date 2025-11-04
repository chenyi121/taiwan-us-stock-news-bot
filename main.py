import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from news_scraper import get_all_news
from trend_analyzer import analyze_trend
from summary_helper import summarize_title
from report_generator import generate_daily_report

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
USER_ID = os.getenv('USER_ID')
print(f"USER_ID 值為：{USER_ID}，型別：{type(USER_ID)}")

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
            msg = f"🌐 {n.get('market')}｜{n.get('source')}\n{title}\n🧠 摘要：{summary}\n📊 趨勢判斷：{trend}\n🔗 {n.get('url')}"
            send_text(msg)
        # 產生報告檔案（可選）
        try:
            pdf = generate_daily_report(enriched)
            print('報告已建立：', pdf)
        except Exception as e:
            print('產生報告失敗：', e)

    if __name__ == '__main__':
        run_push()
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print(f"✅ 使用者 ID：{user_id}")  # 在 Render Logs 可看到
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你的 User ID 是：{user_id}")
    )

if __name__ == "__main__":
    app.run(port=5000)
