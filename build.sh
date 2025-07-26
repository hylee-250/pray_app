#!/usr/bin/env bash
# exit on error
set -o errexit

# Python 버전 확인
python --version

apt-get update
apt-get install -y libpq-dev

# Python 의존성 설치
pip install -r requirements.txt 