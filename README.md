# Python Clean Code 강의 자료

Python 클린 코드 원칙을 설명하기 위한 교육 자료입니다. 로또 번호 생성기를 예제로 사용하여 좋은 코드와 나쁜 코드를 비교합니다.

## 프로젝트 구조

```
clean-code/
├── examples/
│   ├── bad_lottery.py      # 나쁜 코드 예제
│   └── clean_lottery.py    # 클린 코드 예제
├── pyproject.toml          # uv 프로젝트 설정
└── README.md               # 이 파일
```

## 설치 및 실행

이 프로젝트는 [uv](https://github.com/astral-sh/uv)를 사용하여 패키지를 관리합니다.

### 실행 방법

```bash
# 나쁜 코드 예제 실행
uv run examples/bad_lottery.py

# 클린 코드 예제 실행
uv run examples/clean_lottery.py
```

## 코드 비교

### 나쁜 코드 예제 (`bad_lottery.py`)

이 코드는 다음과 같은 클린 코드 원칙을 위반합니다:

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

### 클린 코드 예제 (`clean_lottery.py`)

이 코드는 다음과 같은 클린 코드 원칙을 따릅니다:

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

## 실습 과제

1. `bad_lottery.py`를 직접 실행하고 코드를 분석해보세요
2. `clean_lottery.py`를 실행하고 코드를 비교해보세요
3. 두 코드의 차이점을 직접 나열해보세요
4. 다른 간단한 프로그램을 클린 코드 원칙을 적용하여 리팩토링해보세요

## 참고 자료

- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 라이선스

이 프로젝트는 교육 목적으로 만들어졌습니다.
