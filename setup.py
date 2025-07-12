import os
import json

def set_config(config_path='config.json'):
    required_keys = [
        'OPEN_API_KEY', 'LANGCHAIN_API_KEY',
        'LANGCHAIN_TRACING_V2', 'LANGCHAIN_TRACING',
        'LANGCHAIN_ENDPOINT', 'LANGCHAIN_PROJECT'
    ]

    # 필수값 체크용 딕셔너리 (환경변수명, config key)
    env_map = {
        'OPENAI_API_KEY': 'OPEN_API_KEY',
        'LANGCHAIN_API_KEY': 'LANGCHAIN_API_KEY',
        'LANGCHAIN_TRACING_V2': 'LANGCHAIN_TRACING_V2',
        'LANGCHAIN_TRACING': 'LANGCHAIN_TRACING',
        'LANGCHAIN_ENDPOINT': 'LANGCHAIN_ENDPOINT',
        'LANGCHAIN_PROJECT': 'LANGCHAIN_PROJECT'
    }

    # config 파일 로딩 및 예외처리
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] 설정 파일({config_path})을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print(f"[ERROR] 설정 파일({config_path})이 올바른 JSON 형식이 아닙니다.")
        return

    # 환경변수 세팅 (없으면 경고)
    for env_key, config_key in env_map.items():
        value = config.get(config_key, None)
        if value is not None:
            os.environ[env_key] = str(value)
        else:
            print(f"[WARNING] '{config_key}' 값이 설정 파일에 없습니다. 해당 환경변수는 세팅되지 않습니다.")

    print("[INFO] 환경변수 세팅이 완료되었습니다.")

# 실행 예시
if __name__ == "__main__":
    # 이는 일시적인 환경변수 적용일뿐이다.
    set_config('config.json')
