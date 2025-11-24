from pydantic import ValidationError

from src.lottery07.const import (
    LOTTO_MAX_NUMBER,
    LOTTO_MIN_NUMBER,
    LOTTO_NUMBER_COUNT,
    RANK_BY_MATCH_COUNT,
)
from src.lottery07.generator import AutoLottoGenerator, LottoGenerator
from src.lottery07.model import LottoNumbers, LottoResult

# ===== 도메인 로직 =====
# generate_lotto_numbers()는 generator.py로 이동
# 이제 LottoGenerator 인터페이스를 통해 생성 전략을 주입받습니다


def read_user_numbers(input_func=input, print_func=print) -> LottoNumbers:
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
    return len(set(lotto.numbers) & set(user.numbers))


def get_rank(match_count: int) -> str:
    return RANK_BY_MATCH_COUNT.get(match_count, "fail")


def play_game(
    generator: LottoGenerator,
    input_func=input,
    print_func=print,
) -> LottoResult:
    # 생성 전략을 통해 로또 번호 생성 (어떻게 만드는지는 관심 없음)
    lotto_numbers = generator.generate()
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
    """
    메인 실행 함수

    기본적으로 자동 생성 전략을 사용합니다.
    수동 입력을 원하면 ManualLottoGenerator()로 교체하면 됩니다.
    """
    # 자동 생성 전략 사용
    generator = AutoLottoGenerator()

    # 수동 입력 전략을 원하면 아래 주석 해제
    # from src.lottery07.generator import ManualLottoGenerator
    # generator = ManualLottoGenerator()

    play_game(generator)


if __name__ == "__main__":
    main()
