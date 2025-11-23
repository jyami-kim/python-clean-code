import random
from typing import List


LOTTO_NUMBER_COUNT = 6
LOTTO_MIN_NUMBER = 1
LOTTO_MAX_NUMBER = 45


def generate_lotto_numbers() -> List[int]:
    """로또 당첨 번호를 생성한다."""
    numbers = set()
    while len(numbers) < LOTTO_NUMBER_COUNT:
        numbers.add(random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER))
    return sorted(numbers)


def read_user_numbers() -> List[int]:
    """사용자로부터 로또 번호를 입력받는다."""
    user_numbers: set[int] = set()

    print(f"로또 번호를 입력하세요 ({LOTTO_MIN_NUMBER}~{LOTTO_MAX_NUMBER}, 중복 불가)")

    while len(user_numbers) < LOTTO_NUMBER_COUNT:
        try:
            raw = input(f"{len(user_numbers) + 1}번째 번호: ")
            number = int(raw)
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue

        if not (LOTTO_MIN_NUMBER <= number <= LOTTO_MAX_NUMBER):
            print(f"{LOTTO_MIN_NUMBER}부터 {LOTTO_MAX_NUMBER} 사이의 숫자만 입력 가능합니다.")
            continue

        if number in user_numbers:
            print("이미 입력한 번호입니다. 다른 숫자를 입력해 주세요.")
            continue

        user_numbers.add(number)

    return sorted(user_numbers)


def count_matched_numbers(lotto_numbers: List[int], user_numbers: List[int]) -> int:
    """당첨 번호와 사용자가 선택한 번호 중 일치하는 개수를 반환한다."""
    return len(set(lotto_numbers) & set(user_numbers))


def get_rank(match_count: int) -> str:
    """일치 개수에 따른 순위를 반환한다."""
    if match_count == 6:
        return "1등"
    if match_count == 5:
        return "2등"
    if match_count == 4:
        return "3등"
    if match_count == 3:
        return "4등"
    return "꽝"


def main() -> None:
    lotto_numbers = generate_lotto_numbers()
    user_numbers = read_user_numbers()
    match_count = count_matched_numbers(lotto_numbers, user_numbers)
    rank = get_rank(match_count)

    print("-" * 30)
    print("당첨 번호 :", lotto_numbers)
    print("내 번호   :", user_numbers)
    print(f"일치 개수 : {match_count}개")
    print("결과      :", rank)


if __name__ == "__main__":
    main()