#!/bin/bash
# 確保腳本出錯時立即停止
set -e

echo "=== 1. 激活虛擬環境 ==="
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "未找到 venv 虛擬環境，將使用系統預設 python..."
fi

echo "=== 2. 執行資料庫遷移 ==="
python manage.py migrate

echo "=== 3. 匯入初始資料 ==="
python manage.py loaddata initial_data.json

echo "=== 4. 啟動本機開發伺服器 ==="
python manage.py runserver
