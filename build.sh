#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update
apt-get install -y libpq-dev

# Python 의존성 설치 (Rust 의존성 제거됨)
pip install -r requirements.txt 