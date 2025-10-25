FlashAI v2 — Image → 30s Video + Auto Dubbing (Production Starter)

This package contains production-ready source code (no pretrained model binaries).
Use backend/setup_models_auto.sh and backend/scripts/verify_models.py to help download and verify models.

Quick start (dev):
1. Copy .env.example -> .env and edit.
2. pip install -r requirements.txt
3. bash backend/setup_models_auto.sh  # edit it first to uncomment desired downloads
4. python backend/scripts/verify_models.py
5. docker-compose up --build   # or run run_local.sh for non-docker dev
