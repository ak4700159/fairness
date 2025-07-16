import os
import yaml
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI


""""
config_path에 있는 yaml 파일 기반 프로그램 설정 
- open api키 등록
- langsmith 플랫폼에 프로젝트 등록(추적 및 분석)
"""
def set_config(config_path='config.yaml', project_name='fairness'):
    config_path = get_abs_path(config_path)
    required_keys = [
        'OPEN_API_KEY', 'LANGCHAIN_API_KEY',
        'LANGCHAIN_TRACING_V2', 'LANGCHAIN_TRACING',
        'LANGCHAIN_ENDPOINT', 'LANGCHAIN_PROJECT'
    ]

    # 필수값 체크용 딕셔너리 (환경변수명, config key)
    env_map = {
        'OPENAI_API_KEY': 'OPEN_API_KEY',
        'LANGSMITH_API_KEY': 'LANGSMITH_API_KEY',
        'LANGSMITH_TRACING': 'LANGSMITH_TRACING',
        'LANGSMITH_ENDPOINT': 'LANGSMITH_ENDPOINT',
        # 프로젝트 명은 그때마다 설정 
        # 'LANGSMITH_PROJECT': 'LANGSMITH_PROJECT'
    }

    # config 파일 로딩 및 예외처리
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(f"[ERROR] 설정 파일({config_path})을 찾을 수 없습니다.")
        return
    except yaml.YAMLError:
        print(f"[ERROR] 설정 파일({config_path})이 올바른 YAML 형식이 아닙니다.")
        return

    # 환경변수 세팅 (없으면 경고)
    for env_key, config_key in env_map.items():
        value = config.get(config_key, None)
        if value is not None:
            os.environ[env_key] = str(value)
        else:
            print(f"[WARNING] '{config_key}' 값이 설정 파일에 없습니다. 해당 환경변수는 세팅되지 않습니다.")

    print("[INFO] 환경변수 세팅이 완료되었습니다.")
    logging.langsmith(project_name=project_name)
    

""""
config.json 파일 기반 llm 파라미터 로드 
"""
def load_gpt_model(config_path='config.json'):
    config_path = get_abs_path(config_path)
    # 파일 로딩 
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(f"[ERROR] 설정 파일({config_path})을 찾을 수 없습니다.")
        return
    except yaml.YAMLError:
        print(f"[ERROR] 설정 파일({config_path})이 올바른 YAML 형식이 아닙니다.")
        return
    
    # ChatOpenAI에 매핑
    llm_config = config.get("llm", {})
    if not isinstance(llm_config, dict):
        print("[ERROR] 'llm' 항목이 딕셔너리 형태가 아닙니다.")
        return
    try:
        return ChatOpenAI(**llm_config)
    except TypeError as e:
        print(f"[ERROR] LLM 파라미터 오류: {e}")
    except Exception as e:
        print(f"[ERROR] ChatOpenAI 초기화 중 알 수 없는 오류 발생: {e}")


"""상대 경로를 절대 경로로 변환"""
def get_abs_path(config_path):
    return os.path.abspath(config_path)


# 실행 예시
if __name__ == "__main__":
    # 이는 일시적인 환경변수 적용일뿐이다.
    set_config('config.json')
    llm = load_gpt_model('config.json')