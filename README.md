# 台股 & 美股 智慧新聞 LINE Bot

這個專案會自動抓取台股與美股新聞，使用 OpenAI 產生新聞摘要與趨勢判斷，並透過 LINE Bot 推播。可部署到 Render 並以 Cron Job 定時執行。

## 使用步驟（簡略）
1. 將此專案上傳至 GitHub。
2. 在 Render 建立 Web Service，Build: `pip install -r requirements.txt`，Start: `python main.py`。
3. 在 Render 的 Environment Variables 設定 `.env.example` 中的三個變數。
4. 建立 Cron Job（例如每天 08:30）執行 `python main.py`。

詳細文件請參考程式內註解。
