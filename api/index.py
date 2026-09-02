import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from simulated_data import seed_database
from routes import router

app = FastAPI(
    title="虚拟币行情分析演示系统",
    description="⚠ 仅用于技术学习演示，所有行情、分析、预测全部模拟，绝对不构成投资建议",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on module load
Base.metadata.create_all(bind=engine)
seed_database()

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "虚拟币行情分析演示 API",
        "disclaimer": "⚠ 仅用于技术学习演示，所有行情、分析、预测全部模拟，绝对不构成投资建议。我国不承认虚拟货币，禁止交易。",
        "docs": "/docs",
    }
