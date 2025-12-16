# request-service/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# compose.yamlで設定した環境変数からDB接続URLを取得
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    # フォールバックとして、compose.yamlに書いたURLを使用
    "postgresql://djuser:djpassword@db:5432/djdb" 
)

# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)

# 各リクエストでDBセッションを作成・閉鎖するためのクラス
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMクラスのベースクラス
Base = declarative_base()

# DB接続を管理するための依存性インジェクション関数
# リクエスト処理の開始時にセッションを作成し、終了時に閉じる
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# すべてのテーブルを作成する関数
def create_all_tables():
    # models.py で定義されたすべてのテーブルをDB上に作成（なければ）
    Base.metadata.create_all(bind=engine)
