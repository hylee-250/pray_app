"""
기도앱 버전 정보
"""
import os
import subprocess
from datetime import datetime

__version__ = "1.1.0"
__app_name__ = "기도제목 관리 시스템"

def get_git_version():
    """Git 태그에서 버전 정보를 가져옵니다."""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--exact-match'], 
            capture_output=True, text=True, cwd=os.path.dirname(__file__)
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None

def get_version():
    """버전 정보를 반환합니다. 우선순위: 환경변수 > Git 태그 > 기본값"""
    # 1. 환경변수에서 확인
    env_version = os.getenv("APP_VERSION")
    if env_version:
        return env_version if env_version.startswith('v') else f"v{env_version}"
    
    # 2. Git 태그에서 확인
    git_version = get_git_version()
    if git_version:
        return git_version if git_version.startswith('v') else f"v{git_version}"
    
    # 3. 기본값 사용
    return f"v{__version__}"

def get_full_version():
    """전체 버전 정보를 반환합니다."""
    return f"{__app_name__} {get_version()}"

def get_build_info():
    """빌드 정보를 반환합니다."""
    build_time = datetime.now().strftime("%Y%m%d_%H%M")
    return {
        "version": get_version(),
        "app_name": __app_name__,
        "build_time": build_time,
        "full_version": get_full_version()
    } 