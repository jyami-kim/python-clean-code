# Python Clean Code 강의 자료

Python 클린 코드 원칙을 설명하기 위한 교육 자료입니다. 
단계별 예제와 리팩토링 과정을 통해 클린 코드 작성법을 학습합니다.

## 📚 프로젝트 구조

```
clean-code/
├── src/
│   ├── examples/               # 클린 코드 원칙 예제
│   │   ├── 01.variable.py      # 변수명 작성 원칙
│   │   ├── 02.type_hint.py     # 타입 힌트 사용법
│   │   └── 03.formatting.py    # Ruff를 활용한 포맷팅
│   │
│   ├── lottery04/              # 함수 분리 버전
│   │   ├── __init__.py
│   │   └── game.py
│   │
│   ├── lottery05/              # IO 의존성 제거 버전
│   │   ├── __init__.py
│   │   └── game.py
│   │
│   └── refactoring/            # 단계별 리팩토링 과정
│       ├── 00.bad_lottery.py   # 나쁜 코드 (시작점)
│       ├── 00.clean_lottery.py # 깔끔한 코드 (최종)
│       ├── 01.lottery.py       # Step 1: 기본 구조
│       ├── 02.lottery.py       # Step 2: 함수 분리
│       ├── 03.lottery.py       # Step 3: 상수 추출
│       └── 04.lottery.py       # Step 4: 클래스 설계
│
├── test/                       # 테스트 코드
│   ├── lottery04/
│   │   └── game_test.py
│   └── lottery05/
│       └── game_test.py
│
├── .ruff.toml                  # Ruff 린터/포맷터 설정
├── pyproject.toml              # 프로젝트 설정 (pytest 등)
└── README.md                   # 이 파일
```

## 🚀 설치 및 실행

이 프로젝트는 [uv](https://github.com/astral-sh/uv)를 사용하여 패키지를 관리합니다.

### 설치

```bash
# uv 설치 (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트 클론
git clone https://github.com/jyami-kim/python-clean-code.git
cd python-clean-code
```

### 예제 실행

```bash
# 변수명 작성 원칙
uv run src/examples/01.variable.py

# 타입 힌트 사용법
uv run src/examples/02.type_hint.py

# Ruff 포맷팅 가이드
uv run src/examples/03.formatting.py

# 리팩토링 단계별 코드
uv run src/refactoring/00.bad_lottery.py
uv run src/refactoring/02.lottery.py

# lottery04 (함수 분리)
uv run src/lottery04/game.py

# lottery05 (IO 의존성 제거)
uv run src/lottery05/game.py
```

### 테스트 실행

```bash
# 모든 테스트 실행
uv run pytest

# 특정 테스트만 실행
uv run pytest test/lottery04/
uv run pytest test/lottery05/

# 상세 출력
uv run pytest -v
```

### 코드 검사 및 포맷팅

```bash
# Ruff로 코드 검사
uv run ruff check .

# 자동 수정
uv run ruff check --fix .

# 코드 포맷팅
uv run ruff format .
```

## 📖 학습 내용

### 1. 변수명 작성 원칙 (`01.variable.py`)

**13가지 변수명 원칙:**
1. 의도를 분명히 밝혀라
2. 그릇된 정보를 피하라
3. 의미 있게 구분하라
4. 발음하기 쉬운 이름을 사용하라
5. 검색하기 쉬운 이름을 사용하라
6. 인코딩을 피하라 (헝가리안 표기법 X)
7. 자신의 기억력을 자랑하지 마라
8. 클래스 이름은 명사
9. 메서드 이름은 동사
10. 기발한 이름은 피하라
11. 한 개념에 한 단어를 사용하라
12. 해법 영역과 문제 영역의 이름
13. 의미 있는 맥락을 추가하라

### 2. 타입 힌트 (`02.type_hint.py`)

**타입 힌트를 사용해야 하는 이유:**
- ✅ 팀 협업에서 함수의 의도가 선명해짐
- ✅ 대규모 프로젝트에서 리팩토링 안정성 급증
- ✅ IDE 자동완성이 정확해짐 (생산성 향상)
- ✅ 문서 역할 (Self-Documenting Code)
- ✅ 복잡한 타입도 명확하게 표현 가능

### 3. 코드 포맷팅 (`03.formatting.py`)

**Ruff 활용:**
- 린트 규칙: E (스타일), F (논리 에러), I (import 정렬), N (네이밍), W (경고), UP (최신 문법)
- 자동 포맷팅으로 일관된 코드 스타일 유지
- VS Code 통합으로 저장 시 자동 적용

### 4. 단계별 리팩토링 (`refactoring/`)

**리팩토링 과정:**
1. **00.bad_lottery.py** - 모든 원칙을 위반한 나쁜 코드
2. **01.lottery.py** - 기본 구조 개선
3. **02.lottery.py** - 함수 분리 및 매직 넘버 제거
4. **03.lottery.py** - 상수 추출 및 타입 힌트
5. **04.lottery.py** - 클래스 설계 및 관심사 분리
6. **00.clean_lottery.py** - 최종 클린 코드

### 5. 테스트 가능한 설계

**lottery04 vs lottery05:**
- `lottery04`: 기본 함수 분리
- `lottery05`: IO 의존성 주입으로 테스트 가능한 설계

```python
# lottery05: IO 의존성 주입
def read_user_numbers(input_func=input, print_func=print):
    # 테스트에서 mock 함수를 주입 가능
    pass

# 테스트 코드
def test_valid_input():
    mock_input = Mock(side_effect=["1", "2", "3", "4", "5", "6"])
    numbers = read_user_numbers(input_func=mock_input)
```

## 🎯 나쁜 코드 vs 좋은 코드

### 나쁜 코드 예제 (`00.bad_lottery.py`)

#### ❌ 위반 사항

1. **의미 없는 변수명**
   - `f`, `g`, `n`, `m`, `x`, `l`, `r` 등 단일 문자 변수명
   - 코드를 읽는 사람이 변수의 의미를 파악하기 어려움

2. **함수명이 불명확**
   - `f()`, `g()` - 함수가 무엇을 하는지 전혀 알 수 없음

3. **가독성 없는 코드 스타일**
   - 한 줄에 여러 명령문 작성: `if r not in l:l.append(r)`
   - 공백 없이 빽빽하게 작성된 코드
   - 불필요하게 축약된 표현

4. **매직 넘버**
   - `6`, `1`, `45`, `50`, `100` 등의 하드코딩된 숫자
   - 숫자의 의미를 코드에서 바로 파악할 수 없음

5. **예외 처리 미흡**
   - `except:` - 모든 예외를 무분별하게 catch
   - 구체적인 예외 타입 명시 없음

6. **문서화 부재**
   - 주석이나 docstring 없음
   - 코드의 의도를 파악하기 위해 전체를 분석해야 함

7. **단일 책임 원칙 위반**
   - 함수가 여러 가지 일을 동시에 수행
   - 관심사의 분리가 되어있지 않음

### 좋은 코드 예제 (`00.clean_lottery.py`)

#### ✅ 적용된 원칙

1. **의미 있는 이름 사용**
   ```python
   # Bad
   def f(n,m,x):
   
   # Good
   def generate_single_game(self) -> List[int]:
   ```
   - 함수와 변수의 이름이 그 목적을 명확히 표현
   - `LotteryNumberGenerator`, `generate_single_game` 등

2. **클래스를 통한 관심사 분리**
   - `LotteryNumberGenerator`: 번호 생성 책임
   - `LotteryGamePrinter`: 출력 책임
   - `LotteryGameController`: 전체 흐름 제어 책임

3. **상수 정의**
   ```python
   MIN_NUMBER = 1
   MAX_NUMBER = 45
   NUMBERS_PER_GAME = 6
   ```
   - 매직 넘버를 의미 있는 상수로 대체
   - 유지보수성 향상

4. **함수는 한 가지 일만**
   ```python
   def _generate_unique_numbers(self) -> List[int]:
       """중복 없는 로또 번호를 생성합니다."""
       # 오직 번호 생성만 담당
   
   def _is_duplicate(number: int, existing_numbers: List[int]) -> bool:
       """숫자가 이미 존재하는지 확인합니다."""
       # 오직 중복 검사만 담당
   ```

5. **명확한 문서화**
   - 모듈, 클래스, 함수에 docstring 작성
   - 타입 힌팅 사용 (`-> List[int]`, `count: int`)
   - 의도와 사용법이 명확함

6. **적절한 예외 처리**
   ```python
   except ValueError:
       self._print_invalid_input_error()
   ```
   - 구체적인 예외 타입 명시
   - 의미 있는 에러 메시지 제공

7. **가독성 있는 코드 스타일**
   - 적절한 들여쓰기와 공백
   - 한 줄에 하나의 명령
   - PEP 8 스타일 가이드 준수

8. **작은 함수들**
   - 각 함수가 짧고 이해하기 쉬움
   - 복잡한 로직을 작은 단위로 분해

## 클린 코드 원칙 요약

### 1. 의미 있는 이름
- 변수, 함수, 클래스의 이름이 그 목적을 명확히 드러내야 함
- 단일 문자나 약어보다는 명확한 단어 사용

### 2. 함수는 한 가지 일만
- 각 함수는 하나의 작업만 수행
- 함수가 길어지면 더 작은 함수로 분리

### 3. 중복 제거 (DRY: Don't Repeat Yourself)
- 같은 코드를 반복하지 않음
- 공통 로직은 별도 함수로 추출

### 4. 관심사의 분리
- 각 클래스와 모듈은 명확한 책임을 가짐
- 높은 응집도, 낮은 결합도

### 5. 가독성
- 코드는 글을 읽듯이 자연스럽게 읽혀야 함
- 적절한 공백과 들여쓰기
- 일관된 코딩 스타일

### 6. 문서화
- 복잡한 로직에는 주석 추가
- 모든 공개 API에 docstring 작성
- 타입 힌팅으로 명확성 향상

### 7. 오류 처리
- 구체적인 예외 처리
- 의미 있는 에러 메시지
- 예외 상황을 명확히 처리

### 8. 테스트 가능한 코드
- 작은 단위로 나누어진 함수는 테스트하기 쉬움
- 의존성이 적은 코드 작성

## 📝 테스트 작성

### pytest 사용법

```bash
# 모든 테스트 실행
uv run pytest

# 특정 파일 테스트
uv run pytest test/lottery04/game_test.py

# 상세 출력 (docstring 표시)
uv run pytest -v

# 실패한 테스트만 재실행
uv run pytest --lf
```

### 테스트 예제

```python
class TestIsValidLottoNumber:
    """로또 번호 유효성 검증 테스트"""
    
    def test_valid_number_within_range(self):
        """유효한 범위 내의 번호는 True를 반환한다"""
        assert is_valid_lotto_number(25, [1, 2, 3]) is True
```

**docstring의 역할:**
- 테스트의 의도를 명확히 전달
- pytest `-v` 옵션으로 한글 설명 출력
- `__doc__` 속성으로 프로그래밍 방식 접근 가능

## 🛠️ 개발 도구

### Ruff (린터 & 포맷터)

프로젝트는 `.ruff.toml` 파일로 코드 품질을 관리합니다.

```bash
# 코드 검사
uv run ruff check .

# 자동 수정
uv run ruff check --fix .

# 포맷팅
uv run ruff format .

# 규칙 설명
uv run ruff rule E501
```

### VS Code 설정

`.vscode/settings.json`에 추가하여 저장 시 자동 포맷팅:

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
    }
}
```

## 💡 실습 과제

### 기초
1. `src/examples/01.variable.py` 실행하고 13가지 변수명 원칙 학습
2. `src/examples/02.type_hint.py`로 타입 힌트 필요성 이해
3. `src/refactoring/00.bad_lottery.py`와 `00.clean_lottery.py` 비교

### 중급
4. `src/refactoring/01.lottery.py`부터 `04.lottery.py`까지 단계별 리팩토링 과정 분석
5. `lottery04`와 `lottery05`의 차이점 이해 (IO 의존성 제거)
6. 테스트 코드 작성 연습

### 고급
7. 자신의 코드에 Ruff 적용하여 자동 개선
8. 기존 프로젝트를 클린 코드 원칙으로 리팩토링
9. 테스트 가능한 설계로 코드 재구성

## 📚 참고 자료

### 책
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Refactoring by Martin Fowler](https://refactoring.com/)

### 공식 문서
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

### 관련 블로그
- [Clean Code - 변수명 작성법](https://jyami.tistory.com/74)

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

## 📄 라이선스

이 프로젝트는 교육 목적으로 만들어졌습니다.

## 👨‍💻 Author

**jyami-kim**
- GitHub: [@jyami-kim](https://github.com/jyami-kim)
- Blog: [jyami.tistory.com](https://jyami.tistory.com)
