# Python Clean Code 강의 자료

Python 클린 코드 원칙을 설명하기 위한 교육 자료입니다. 로또 번호 생성기를 예제로 사용하여 좋은 코드와 나쁜 코드를 비교하고, 점진적으로 리팩토링하며 실전 패턴(의존성 분리, 전략 패턴, 테스트, 주석 등)을 학습합니다.

## 프로젝트 구조

```
clean-code/
├── src/
│   ├── examples/
│   │   ├── 01.variable.py      # 변수명 원칙 예제
│   │   ├── 02.type_hint.py     # 타입 힌트 예제
│   │   ├── 03.formatting.py    # 코드 포매팅 예제
│   │   └── 04.comment.py       # 주석 원칙 예제
│   ├── lottery04/              # 함수 분리 버전
│   ├── lottery05/              # IO 의존성 분리 버전
│   ├── lottery06/              # Pydantic 도메인 모델 적용
│   ├── lottery07/              # 전략 패턴(Generator) + 의존성 분리
│   └── refactoring/            # 단계별 리팩토링 예제
├── test/
│   ├── lottery04/
│   ├── lottery05/
│   ├── lottery06/
│   └── lottery07/
├── pyproject.toml              # uv/pytest 설정
├── .ruff.toml                  # Ruff 포매터/린터 설정
└── README.md                   # 이 파일
```

## 설치 및 실행

이 프로젝트는 [uv](https://github.com/astral-sh/uv)를 사용하여 패키지를 관리합니다.

### 실행 방법

```bash
# 예제 실행 (src/examples)
uv run python src/examples/01.variable.py
uv run python src/examples/02.type_hint.py
uv run python src/examples/03.formatting.py
uv run python src/examples/04.comment.py

# 리팩토링 단계별 실행 (lottery04~07)
uv run python -m src.lottery04.game
uv run python -m src.lottery05.game
uv run python -m src.lottery06.game
uv run python -m src.lottery07.game

# 테스트 실행
uv run pytest -v
```

## 예제별 주요 학습 포인트

#### 1. 변수명 원칙 (`src/examples/01.variable.py`)
- 13가지 변수명 클린 코드 원칙과 예시
- 의미 있는 이름, 헝가리언 표기법 지양, 구체적/추상적 이름 구분 등

#### 2. 타입 힌트 (`src/examples/02.type_hint.py`)
- 타입 힌트의 장점, 코드 안정성, IDE 지원, 리팩토링 용이성 등
- 실제 쇼핑카트 예제 포함

#### 3. 코드 포매팅 (`src/examples/03.formatting.py`)
- Ruff 포매터/린터 사용법, 주요 규칙(E,F,I,N,W,UP) 예시
- VS Code 연동 방법, 워크플로우

#### 4. 주석 원칙 (`src/examples/04.comment.py`)
- 나쁜 주석/좋은 주석/필요 없는 주석/도메인 주석/법적 주석/TODO/마커 등
- "주석은 최후의 수단" 원칙, Before/After 예시, 체크리스트

#### 5. 단계별 리팩토링 (lottery04~07)
- 함수 분리 → IO 분리 → 도메인 모델(Pydantic) → 전략 패턴(Generator)
- 각 단계별 테스트 코드 포함

#### 6. 전략 패턴 & 의존성 분리 (`src/lottery07/generator.py`)
- `LottoGenerator` Protocol로 인터페이스 분리
- `AutoLottoGenerator`, `ManualLottoGenerator`, `FixedLottoGenerator` 구현
- 게임 로직은 생성 전략에만 의존 (OCP, DIP)
- 테스트에서 FakeGenerator로 주입 가능

#### 7. 테스트 코드 (`test/lottery04~07/`)
- pytest 기반, Mock 활용, 도메인 모델/로직/생성 전략 검증

## 클린 코드 원칙 요약

1. 의미 있는 이름
2. 함수는 한 가지 일만
3. 중복 제거 (DRY)
4. 관심사의 분리
5. 가독성
6. 문서화
7. 오류 처리
8. 테스트 가능한 코드

## 실습 과제

1. 각 예제 파일을 직접 실행하고 코드를 분석해보세요
2. 단계별 리팩토링(04~07)을 따라가며 구조 변화를 체험해보세요
3. 테스트 코드를 직접 실행해보고, 실패/성공 케이스를 추가해보세요
4. 주석 원칙 예제를 참고해 자신의 코드에 적용해보세요
5. 다른 프로그램을 클린 코드 원칙에 따라 리팩토링해보세요

## 참고 자료

- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 라이선스

이 프로젝트는 교육 목적으로 만들어졌습니다.
