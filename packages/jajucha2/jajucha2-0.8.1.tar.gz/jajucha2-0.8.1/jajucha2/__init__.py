# from . import control,camera,ai

# __init__.py
import sys

# 특정 모듈만 임포트하는 경우 로딩을 제한합니다.
if "jajucha2" in sys.modules:
    from . import control, camera, ai