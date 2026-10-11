#!/usr/bin/env bash
set -euo pipe fail # gagal di satu baris = script berhenti. Fail fast.

cd /home/deploy/minimart-api
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart minimart
sleep 3
curl -f http://127.0.0.1:8000/health # -f = gagal kalau HTTP error
echo "Deploy OK"
