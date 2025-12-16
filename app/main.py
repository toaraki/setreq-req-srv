# request-service/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# 新しく作成したモジュールをインポート
from . import models, schemas, database 

# DB接続とテーブル作成を最初に実行
database.create_all_tables() 

app = FastAPI()

# -----------------------------------------------------------------
# CORS設定 (前回設定済み)
# -----------------------------------------------------------------
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# データベース操作の関数 (DB操作を分離する役割)
# -----------------------------------------------------------------
def create_request(db: Session, request: schemas.RequestCreate):
    """新しいリクエストをDBに保存する"""
    db_request = models.DjRequest(
        title=request.title,
        artist=request.artist,
        requester_name=request.requester_name
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request) # DBからIDなどの最新情報を取得
    return db_request

def get_requests(db: Session, skip: int = 0, limit: int = 100):
    """すべてのリクエストを取得する"""
    return db.query(models.DjRequest).offset(skip).limit(limit).all()

# -----------------------------------------------------------------
# APIエンドポイント
# -----------------------------------------------------------------

@app.get("/health")
def health_check():
    """Health Check (Liveness/Readiness Probe用)"""
    return {"status": "ok"}

@app.get("/requests", response_model=List[schemas.Request])
def read_requests(db: Session = Depends(database.get_db)):
    """リクエスト一覧を取得するエンドポイント（DB接続版）"""
    requests = get_requests(db)
    return requests

@app.post("/requests", response_model=schemas.Request)
def add_request(request: schemas.RequestCreate, db: Session = Depends(database.get_db)):
    """新しいリクエストを登録するエンドポイント"""
    return create_request(db=db, request=request)
