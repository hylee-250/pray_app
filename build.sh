#!/usr/bin/env bash
# exit on error
set -o errexit

# PostgreSQL 클라이언트 라이브러리 설치
apt-get update
apt-get install -y libpq-dev

# Python 의존성 설치
pip install -r requirements.txt 