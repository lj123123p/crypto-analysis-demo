from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta

from database import get_db
from models import MarketData
from simulated_data import simulate_ai_analysis

router = APIRouter(prefix="/api", tags=["market"])


@router.get("/history/{coin}")
def get_history(
    coin: str,
    days: int = Query(90, ge=1, le=365),
    db: Session = Depends(get_db),
):
    coin = coin.upper()
    valid = {"BTC", "ETH", "SOL", "BNB"}
    if coin not in valid:
        raise HTTPException(400, f"Invalid coin, choose from {valid}")

    cutoff = datetime.now() - timedelta(days=days)
    rows = (
        db.query(MarketData)
        .filter(MarketData.coin == coin, MarketData.timestamp >= cutoff)
        .order_by(MarketData.timestamp.asc())
        .all()
    )

    if not rows:
        raise HTTPException(404, f"No data for {coin}")

    return {
        "coin": coin,
        "days": days,
        "disclaimer": "所有数据均为模拟生成，不构成任何投资建议",
        "data": [
            {
                "time": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp": int(r.timestamp.timestamp() * 1000),
                "open": r.open,
                "high": r.high,
                "low": r.low,
                "close": r.close,
                "volume": r.volume,
            }
            for r in rows
        ],
    }


@router.post("/analyze")
def analyze(body: dict, db: Session = Depends(get_db)):
    coin = body.get("coin", "BTC").upper()
    news = body.get("news", "").strip()

    valid = {"BTC", "ETH", "SOL", "BNB"}
    if coin not in valid:
        raise HTTPException(400, f"Invalid coin, choose from {valid}")

    rows = (
        db.query(MarketData)
        .filter(MarketData.coin == coin)
        .order_by(desc(MarketData.timestamp))
        .limit(30)
        .all()
    )
    rows.reverse()

    if not rows:
        raise HTTPException(404, f"No data for {coin}")

    result = simulate_ai_analysis(coin, news, rows)
    return result


@router.get("/coins")
def list_coins():
    return {
        "coins": [
            {"symbol": "BTC", "name": "Bitcoin"},
            {"symbol": "ETH", "name": "Ethereum"},
            {"symbol": "SOL", "name": "Solana"},
            {"symbol": "BNB", "name": "BNB"},
        ],
        "disclaimer": "所有数据均为模拟生成，不构成任何投资建议",
    }
