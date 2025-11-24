"""
Lottery Game Package (IO 의존성 제거 버전)
로또 게임 패키지 - 테스트 가능한 설계
"""

from .const import (
    LOTTO_MAX_NUMBER,
    LOTTO_MIN_NUMBER,
    LOTTO_NUMBER_COUNT,
    RANK_BY_MATCH_COUNT,
)
from .game import (
    count_match,
    generate_lotto_numbers,
    get_rank,
    play_game,
    read_user_numbers,
)
from .model import LottoNumbers, LottoResult

__all__ = [
    "generate_lotto_numbers",
    "read_user_numbers",
    "count_match",
    "get_rank",
    "play_game",
    "LOTTO_NUMBER_COUNT",
    "LOTTO_MIN_NUMBER",
    "LOTTO_MAX_NUMBER",
    "RANK_BY_MATCH_COUNT",
    "LottoNumbers",
    "LottoResult",
]
