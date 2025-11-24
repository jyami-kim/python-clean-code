import random

from pydantic import ValidationError

from src.lottery06.const import (
    LOTTO_MAX_NUMBER,
    LOTTO_MIN_NUMBER,
    LOTTO_NUMBER_COUNT,
    RANK_BY_MATCH_COUNT,
)
from src.lottery06.model import LottoNumbers, LottoResult


# ===== 도메인 로직 =====
def generate_lotto_numbers() -> LottoNumbers:
    """랜덤 로또 번호 6개 생성 후, Pydantic으로 검증"""
    numbers: list[int] = []
    while len(numbers) < LOTTO_NUMBER_COUNT:
        candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
        if candidate in numbers:
            continue
        numbers.append(candidate)

    return LottoNumbers(numbers=numbers)


def read_user_numbers(input_func=input, print_func=print) -> LottoNumbers:
    """
    사용자 입력을 받아 LottoNumbers 모델 생성
    - 쉼표(,)로 구분해서 6개 입력
    - Pydantic이 개수/범위/중복 검증을 수행
    """
    while True:
        raw = input_func(
            f"{LOTTO_NUMBER_COUNT}개의 번호를 콤마(,)로 구분해서 입력하세요 ({LOTTO_MIN_NUMBER}~{LOTTO_MAX_NUMBER}): "
        )

        try:
            parts = [p.strip() for p in raw.split(",")]
            numbers = [int(p) for p in parts]
        except ValueError:
            print_func("숫자만 입력해 주세요.")
            continue

        try:
            return LottoNumbers(numbers=numbers)
        except ValidationError as e:
            print_func("입력값이 올바르지 않습니다:")
            for err in e.errors():
                # 예: numbers.0 -> 첫 번째 번호
                loc = ".".join(str(x) for x in err["loc"])
                print_func(f"- {loc}: {err['msg']}")
            print_func("다시 입력해 주세요.\n")


def count_match(lotto: LottoNumbers, user: LottoNumbers) -> int:
    """일치하는 숫자 개수 계산 (도메인 모델 사용)"""
    return len(set(lotto.numbers) & set(user.numbers))


def get_rank(match_count: int) -> str:
    """일치 개수 → 등수 문자열"""
    return RANK_BY_MATCH_COUNT.get(match_count, "fail")


def play_game(input_func=input, print_func=print) -> LottoResult:
    """로또 게임 한 판 실행 후 LottoResult 반환"""

    lotto_numbers = generate_lotto_numbers()
    user_numbers = read_user_numbers(input_func=input_func, print_func=print_func)
    match_count = count_match(lotto_numbers, user_numbers)
    rank = get_rank(match_count)

    result = LottoResult(
        lotto_numbers=lotto_numbers,
        user_numbers=user_numbers,
        match_count=match_count,
        rank=rank,
    )

    # 출력은 별도 (도메인 모델과 IO 분리)
    print_func(f"result: {result.lotto_numbers.numbers}")
    print_func(f"mine:   {result.user_numbers.numbers}")
    print_func(f"match:  {result.match_count}")
    print_func(f"rank:   {result.rank}")

    return result


def main() -> None:
    play_game()


if __name__ == "__main__":
    main()
