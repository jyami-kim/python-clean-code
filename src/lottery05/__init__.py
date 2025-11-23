"""
Lottery Game Package (IO 의존성 제거 버전)
로또 게임 패키지 - 테스트 가능한 설계
"""

from .game import (
    is_valid_lotto_number,
    generate_lotto_numbers,
    read_user_numbers,
    count_match,
    get_rank,
    print_result,
    LOTTO_NUMBER_COUNT,
    LOTTO_MIN_NUMBER,
    LOTTO_MAX_NUMBER,
    RANK_BY_MATCH_COUNT,
)

__all__ = [
    "is_valid_lotto_number",
    "generate_lotto_numbers",
    "read_user_numbers",
    "count_match",
    "get_rank",
    "print_result",
    "LOTTO_NUMBER_COUNT",
    "LOTTO_MIN_NUMBER",
    "LOTTO_MAX_NUMBER",
    "RANK_BY_MATCH_COUNT",
]
