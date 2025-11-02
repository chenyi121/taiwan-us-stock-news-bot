def analyze_trend(text):
    if not text:
        return "⚖️ 中性"
    bullish = ['上漲','創高','利多','成長','回升','反彈','看好','利好','強勁']
    bearish = ['下跌','利空','衰退','崩跌','賣壓','走弱','疲軟','利空消息','走低']
    score = 0
    lower = text.lower()
    for w in bullish:
        if w in text or w.lower() in lower:
            score += 1
    for w in bearish:
        if w in text or w.lower() in lower:
            score -= 1
    if score > 0:
        return '📈 上漲趨勢'
    if score < 0:
        return '📉 下跌趨勢'
    return '⚖️ 中性'
