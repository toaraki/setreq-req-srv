# request-service/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 必須の環境変数として取得。設定されていない場合は None になる
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # ローカル開発で環境変数を忘れている場合に気づけるようにする
    # print("Warning: DATABASE_URL is not set.")
    raise RuntimeError("DATABASE_URL must be set")


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
