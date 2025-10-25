#!/usr/bin/env bash
set -euo pipefail
echo "FlashAI v2 - setup models helper (edit to match your chosen models)"
ROOT="$(cd "$(dirname "$0")" && pwd)/.."
MODELS_DIR="${ROOT}/models"
mkdir -p "$MODELS_DIR"
echo "[*] Models directory: $MODELS_DIR"
echo "[*] Please edit this script to add exact HF repo IDs or Google Drive IDs for checkpoints."
echo "[*] Example usage: export HF_TOKEN=xxxx && bash backend/setup_models_auto.sh"
# This script intentionally leaves download entries as examples for safety/licensing reasons.
