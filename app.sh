#!/bin/bash
# uvicorn を使用して app/main.py の app インスタンスを起動
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
