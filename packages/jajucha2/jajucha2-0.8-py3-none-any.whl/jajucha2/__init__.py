# from . import control,camera,ai
# __init__.py

# 모든 모듈을 로드하는 함수를 정의합니다.
def load_all():
    global control, camera, ai
    from . import control, camera, ai

# `import jajucha2`로 모든 모듈을 로드할 때 `load_all`을 호출합니다.
load_all()