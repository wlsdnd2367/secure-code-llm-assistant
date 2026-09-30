# SecureCode LLM Assistant

파이썬 코드의 SQL Injection과 Command Injection 가능성을 분석하고,
원인 설명과 시큐어 코딩 패치를 제안하는 RAG 기반 LLM 보안 도구입니다.

웹 해킹을 공부하며 취약점을 찾는 단계에서 더 나아가, 취약한 코드를
안전한 코드로 수정하는 과정까지 학습하기 위해 만들었습니다.

## 주요 기능

- 파이썬 소스 코드 입력과 Streamlit 기반 로컬 UI
- SQL Injection·Command Injection 원인 분석
- 시큐어 코딩 패치 제안
- `secure_coding_guide.txt` 기반 RAG
- `all-MiniLM-L6-v2` 로컬 임베딩과 Chroma 벡터 검색
- Gemini API를 이용한 분석 결과 생성

## 구조

```text
사용자 코드
  -> 시큐어 코딩 가이드 검색
  -> 관련 가이드 조각과 코드를 프롬프트에 구성
  -> Gemini 분석
  -> 취약점 원인과 패치 코드 출력
```

이 프로젝트는 LLM을 직접 학습하거나 로컬에서 구동하지 않습니다.
앱·임베딩·벡터 검색은 로컬에서 실행되며, 답변 생성은 Gemini API를 사용합니다.

## 실행 방법

Python 3.11 이상을 권장합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
```

`.env`에 자신의 Google API 키와 사용 모델을 설정한 뒤 실행합니다.

```bash
streamlit run app.py
```

## 검증

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q app.py list_models.py security_config.py
```

## 현재 범위와 한계

- 현재 가이드는 SQL Injection과 Command Injection을 다룹니다.
- LLM의 제안은 완전한 보안 검증을 대신하지 않으며, 수정 코드는 반드시 사람이 검토해야 합니다.
- 입력한 코드는 Gemini API로 전송되므로 비밀정보나 민감한 소스 코드를 입력하면 안 됩니다.
- 공격 패턴과 안전한 코드 예시를 확장하고, 결과를 정량적으로 평가하는 작업이 추가로 필요합니다.

## 보안

API 키는 소스 코드에 저장하지 않고 `.env`의 `GOOGLE_API_KEY`로만 전달합니다.
`.env`는 Git에서 제외됩니다. 키가 노출됐다면 즉시 폐기하고 재발급
