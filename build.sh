#!/usr/bin/env bash
# exit on error
set -o errexit

# Python 의존성 설치 (Rust 의존성 제거됨)
pip install -r requirements.txt 