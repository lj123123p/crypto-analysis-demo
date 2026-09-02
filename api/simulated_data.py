import random
from datetime import datetime, timedelta
from models import MarketData
from database import SessionLocal

COINS = {
    "BTC": 50000.0,
    "ETH": 3000.0,
    "SOL": 150.0,
    "BNB": 300.0,
}

COIN_NAMES = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "BNB": "BNB",
}


def generate_ohlcv(coin: str, days: int = 365):
    base_price = COINS[coin]
    price = base_price
    records = []
    now = datetime.now()

    for i in range(days):
        t = now - timedelta(days=days - i)
        t = t.replace(hour=random.randint(0, 23), minute=0, second=0, microsecond=0)

        change = random.gauss(0.0005, 0.025)
        open_price = round(price, 2)
        close_price = round(open_price * (1 + change), 2)
        high_price = round(max(open_price, close_price) * (1 + abs(random.gauss(0, 0.008))), 2)
        low_price = round(min(open_price, close_price) * (1 - abs(random.gauss(0, 0.008))), 2)
        volume = round(random.uniform(1000, 30000), 2)

        records.append(MarketData(
            coin=coin,
            timestamp=t,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=volume,
        ))
        price = close_price

    return records


def seed_database():
    db = SessionLocal()
    existing = db.query(MarketData).count()
    if existing == 0:
        for coin in COINS:
            records = generate_ohlcv(coin)
            for r in records:
                db.add(r)
            print(f"  [seed] {coin}: {len(records)} records generated")
        db.commit()
    else:
        print(f"  [seed] database already has {existing} records, skip seeding")
    db.close()


def recent_trend(data_rows):
    if len(data_rows) < 5:
        return "平稳"
    closes = [r.close for r in data_rows[-5:]]
    pct = (closes[-1] - closes[0]) / closes[0] * 100
    if pct > 3:
        return "上涨"
    if pct < -3:
        return "下跌"
    return "震荡"


def compute_ma(data_rows, period):
    if len(data_rows) < period:
        return None
    closes = [r.close for r in data_rows[-period:]]
    return sum(closes) / period


def compute_rsi(data_rows, period=14):
    if len(data_rows) < period + 1:
        return 50.0
    gains, losses = 0.0, 0.0
    for i in range(-period, 0):
        diff = data_rows[i].close - data_rows[i - 1].close
        if diff > 0:
            gains += diff
        else:
            losses -= diff
    if losses == 0:
        return 100.0
    rs = gains / losses
    return round(100 - 100 / (1 + rs), 1)


def simulate_ai_analysis(coin: str, news_text: str, data_rows: list):
    trend = recent_trend(data_rows)
    rsi = compute_rsi(data_rows)
    ma5 = compute_ma(data_rows, 5)
    ma20 = compute_ma(data_rows, 20)
    last_close = data_rows[-1].close if data_rows else 0

    pos_kw = ["利好", "涨", "突破", "增长", "采用", "合规", "ETF", "机构", "牛", "做多", "升级", "生态"]
    neg_kw = ["利空", "跌", "监管", "禁止", "黑客", "攻击", "暴跌", "熊", "做空", "风险", "诉讼", "漏洞"]

    score = 0
    text_lower = news_text.lower()
    for kw in pos_kw:
        if kw in text_lower:
            score += 1
    for kw in neg_kw:
        if kw in text_lower:
            score -= 1.5

    sentiment = "中性"
    if score > 2:
        sentiment = "偏多"
    elif score > 0:
        sentiment = "略偏多"
    elif score < -2:
        sentiment = "偏空"
    elif score < 0:
        sentiment = "略偏空"

    lines = []
    lines.append(f"【模拟AI分析 - {coin}({COIN_NAMES[coin]})】")
    lines.append(f"⚠ 以下内容为模拟推演，不构成任何投资建议 ⚠")
    lines.append("")

    lines.append(f"■ 当前价格: {last_close:.2f} USDT")
    lines.append(f"■ 近期趋势: {trend}")
    lines.append(f"■ RSI(14): {rsi} {'(超买区)' if rsi > 70 else '(超卖区)' if rsi < 30 else '(正常区间)'}")
    if ma5 and ma20:
        lines.append(f"■ MA5: {ma5:.2f}  |  MA20: {ma20:.2f}")
        lines.append(f"■ 均线形态: {'多头排列' if ma5 > ma20 else '空头排列' if ma5 < ma20 else '交织'}")
    lines.append(f"■ 新闻情绪: {sentiment} (情绪得分: {score:+.1f})")
    lines.append("")

    pred_direction = "震荡"
    pred_confidence = "低"
    if sentiment == "偏多" and trend == "上涨":
        pred_direction = "震荡偏多"
        pred_confidence = "中"
    elif sentiment == "偏空" or trend == "下跌":
        pred_direction = "震荡偏空"
        pred_confidence = "中"
    if score > 3 and trend == "上涨":
        pred_direction = "看多"
        pred_confidence = "高"
    elif score < -3 and trend == "下跌":
        pred_direction = "看空"
        pred_confidence = "高"

    lines.append(f"■ 模拟预测方向: {pred_direction}")
    lines.append(f"■ 模拟置信度: {pred_confidence}")
    lines.append("")

    support = round(last_close * (1 - random.uniform(0.03, 0.08)), 2)
    resist = round(last_close * (1 + random.uniform(0.03, 0.08)), 2)
    lines.append(f"■ 模拟支撑位: {support} USDT")
    lines.append(f"■ 模拟阻力位: {resist} USDT")
    lines.append("")

    summary = (
        f"综合新闻情绪「{sentiment}」与近期走势「{trend}」，"
        f"模拟模型预测短期行情以{pred_direction}为主（置信度{pred_confidence}）。"
        f"当前RSI为{rsi}，市场情绪一般。请注意：以上所有内容均为模拟推演，"
        f"虚拟货币交易在我国不受法律保护，请勿据此进行真实交易。"
    )
    lines.append(f"■ 综合评述: {summary}")

    return {
        "coin": coin,
        "coin_name": COIN_NAMES[coin],
        "current_price": last_close,
        "trend": trend,
        "rsi": rsi,
        "sentiment": sentiment,
        "sentiment_score": score,
        "prediction": pred_direction,
        "confidence": pred_confidence,
        "support": support,
        "resistance": resist,
        "summary": summary,
        "analysis_text": "\n".join(lines),
        "disclaimer": "⚠ 以上所有分析内容均为模拟推演，不构成任何投资建议。我国不承认虚拟货币，禁止交易。",
    }
