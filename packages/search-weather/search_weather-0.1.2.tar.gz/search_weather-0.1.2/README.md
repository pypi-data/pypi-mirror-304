# Search Weather

Search Weather는 사용자의 자연어 쿼리를 기반으로 날씨 정보를 검색하고 제공하는 파이썬 패키지입니다. 이 패키지는 사용자가 일상적인 언어로 날씨 정보를 요청할 수 있도록 설계되었으며, 위치와 날짜 정보를 자동으로 추출하여 정확한 날씨 정보를 제공합니다. OpenWeatherMap API를 활용하여 신뢰할 수 있는 날씨 데이터를 제공하며, 이를 이해하기 쉬운 자연어 형태로 변환하여 사용자에게 전달합니다.

### 주요 기능

- **자연어 쿼리 처리**: 사용자가 입력한 자연어 쿼리를 이해하고, 필요한 정보를 추출합니다.
- **정확한 날씨 정보 제공**: OpenWeatherMap API를 통해 실시간 날씨 데이터를 가져와 사용자에게 제공합니다.
- **위도 및 경도 추출**: 지역 이름을 통해 위도와 경도를 추출하여 날씨 정보를 조회합니다.
- **다양한 언어 지원**: 한국어를 포함한 여러 언어로 날씨 정보를 제공합니다.
- **사용자 친화적인 출력**: 날씨 정보를 이해하기 쉬운 형태로 변환하여 출력합니다.

### 사용 사례

- 사용자가 "내일 서울의 날씨는 어때?"라고 질문하면, 패키지는 서울의 내일 날씨 정보를 자동으로 검색하여 사용자에게 제공합니다.
- 특정 날짜와 위치에 대한 날씨 정보를 요청할 수 있습니다.

### 기술 스택

- **Python**: 패키지의 주요 프로그래밍 언어
- **OpenWeatherMap API**: 날씨 데이터 제공
- **spaCy**: 자연어 처리 라이브러리 (한국어 모델 포함)
- **Geopy**: 지역 이름을 통해 위도와 경도를 추출하는 라이브러리
- **pytest**: 테스트 프레임워크


## 한계

- **언어 지원**: 현재 이 패키지는 한국어만 지원합니다. 다른 언어로의 쿼리는 처리할 수 없습니다.
- **형식 제한**: 사용자가 입력하는 쿼리는 정해진 형식에서 많이 벗어나면 지역 또는 시간 정보를 파싱하지 못해 날씨 데이터를 조회하지 못할 수 있습니다. 예를 들어, "서울의 날씨" 대신 "서울"이라고만 입력하면 올바른 결과를 제공하지 못할 수 있습니다.
- **API 의존성**: OpenWeatherMap API의 가용성에 따라 날씨 정보의 정확성과 신뢰성이 달라질 수 있습니다. API 호출 제한에 도달하면 추가 요청이 실패할 수 있습니다.

## 아키텍처

이 프로젝트는 다음과 같은 구조로 구성되어 있습니다:

```

search_weather/
│
├── __init__.py          # 패키지 초기화 파일
├── api.py               # OpenWeatherMap API와의 통신을 담당
├── parser.py            # 자연어 쿼리 파싱을 담당
├── weather.py           # 날씨 정보 처리 및 변환
└── utils.py             # 유틸리티 함수들
```

### 동작원리

1. **사용자 입력**: 사용자가 자연어 쿼리(예: "내일 서울의 날씨는 어때?")를 입력합니다.
2. **쿼리 파싱**: `parse_query.py`에서 자연어 쿼리를 분석하여 필요한 정보(위치, 날짜 등)를 추출하고 위치 이름을 통해서 `geopy`를 사용하여 위도와 경도를 구합니다.
3. **API 호출**: `get_weather.py`에서 OpenWeatherMap API를 호출하여 해당 위치의 날씨 정보를 요청하고, API로부터 받은 날씨 데이터를 처리합니다.
4. **데이터 처리**: `generate_natural_language_response`에서 사용자에게 이해하기 쉬운 형태로 변환합니다.
5. **결과 출력**: 최종적으로 변환된 날씨 정보를 사용자에게 출력합니다.

## 사용하기

### 설치

pip를 사용하여 설치:

```bash
pip install search-weather
```

또는 poetry를 사용하여 설치:

```bash
poetry add search-weather
```

### 기본 사용법

```python
from search_weather import set_api_key, query

# OpenWeatherMap API 키 설정
set_api_key("your_api_key_here")

# 날씨 쿼리 실행
result = query("내일 서울의 날씨는 어때")
print(result)
```

### 주의사항

- OpenWeatherMap API 키가 필요합니다. [OpenWeatherMap](https://openweathermap.org/)에서 무료로 API 키를 발급받을 수 있습니다.
- 처음 사용 시 한국어 언어 모델(ko_core_news_sm)을 자동으로 다운로드합니다. 인터넷 연결이 필요하며 다운로드에 시간이 걸릴 수 있습니다.

## 테스트하기

이 프로젝트는 pytest를 사용하여 테스트를 실행합니다. 테스트를 실행하려면 다음 단계를 따르세요:

1. 프로젝트 루트 디렉토리로 이동합니다.
2. 필요한 의존성을 설치합니다: `poetry install`
3. 다음 명령어로 테스트를 실행합니다: `pytest tests/`

주요 테스트 케이스:
- API 키 설정 및 조회 테스트
- 쿼리 파싱 테스트
- 위치 정보 변환 테스트
- 날씨 정보 조회 테스트
- 전체 프로세스 테스트
- 에러 처리 테스트

## Package 만들기

이 프로젝트를 패키지로 만들어 배포하려면 다음 단계를 따르세요:

1. 프로젝트 구조 확인:
   - 모든 필요한 파일들이 올바른 위치에 있는지 확인합니다.

2. setup.py 또는 pyproject.toml 파일 최종 확인:
   - 버전 번호, 의존성, 메타데이터 등이 올바른지 확인합니다.

3. 패키지 빌드:
   - setup.py 사용 시: `python deploy.py`
   - poetry 사용 시: `poetry build`

4. PyPI에 배포:
   - setup.py 사용 시:
     ```
     pip install twine
     twine upload dist/*
     ```
   - poetry 사용 시: `poetry publish`

5. 배포 확인:
   - PyPI 페이지에서 패키지가 올바르게 등록되었는지 확인합니다.

6. 테스트 설치:
   - 새로운 가상 환경에서 `pip install search_weather` 또는 `poetry add search_weather`로 설치해봅니다.

패키지를 만들고 배포한 후에는 지속적인 관리와 업데이트가 필요합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

프로젝트 관리자: [minarae](mailto:minarae@gmail.com)

프로젝트 홈페이지: [https://github.com/minarae/search_weather](https://github.com/minarae/search_weather)
