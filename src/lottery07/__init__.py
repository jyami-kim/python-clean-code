"""
Lottery Game Package (전략 패턴 적용 버전)
로또 게임 패키지 - 생성 전략 분리

클린 코드 개선점:
- Strategy Pattern: 로또 번호 생성 전략을 인터페이스로 분리
- Dependency Inversion: 구체 구현이 아닌 LottoGenerator Protocol에 의존
- Open-Closed Principle: 새로운 생성 전략 추가 시 기존 코드 수정 불필요
"""

from .const import (
    LOTTO_MAX_NUMBER,
    LOTTO_MIN_NUMBER,
    LOTTO_NUMBER_COUNT,
    RANK_BY_MATCH_COUNT,
)
from .game import (
    count_match,
    get_rank,
    play_game,
    read_user_numbers,
)
from .generator import (
    AutoLottoGenerator,
    FixedLottoGenerator,
    LottoGenerator,
    ManualLottoGenerator,
)
from .model import LottoNumbers, LottoResult

__all__ = [
    # 게임 로직
    "read_user_numbers",
    "count_match",
    "get_rank",
    "play_game",
    # 생성 전략
    "LottoGenerator",
    "AutoLottoGenerator",
    "ManualLottoGenerator",
    "FixedLottoGenerator",
    # 상수
    "LOTTO_NUMBER_COUNT",
    "LOTTO_MIN_NUMBER",
    "LOTTO_MAX_NUMBER",
    "RANK_BY_MATCH_COUNT",
    # 모델
    "LottoNumbers",
    "LottoResult",
]
