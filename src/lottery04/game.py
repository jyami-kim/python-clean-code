import random

# 상수 분리 (매직 넘버 제거)
LOTTO_NUMBER_COUNT = 6
LOTTO_MIN_NUMBER = 1
LOTTO_MAX_NUMBER = 45

# 등급 매핑
RANK_BY_MATCH_COUNT = {
    6: "1st",
    5: "2nd",
    4: "3rd",
    3: "4th",
}


def is_valid_lotto_number(number: int, existing_numbers: list[int]) -> bool:
    """로또 번호로 유효한지 검사한다."""
    return (
        LOTTO_MIN_NUMBER <= number <= LOTTO_MAX_NUMBER
        and number not in existing_numbers
    )


def generate_lotto_numbers() -> list[int]:
    """로또 번호 6개 생성"""
    lotto_numbers: list[int] = []
    while len(lotto_numbers) < LOTTO_NUMBER_COUNT:
        candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
        if not is_valid_lotto_number(candidate, lotto_numbers):
            continue
        lotto_numbers.append(candidate)
    return lotto_numbers


def read_user_numbers() -> list[int]:
    """사용자 번호 입력 + 검증"""
    user_numbers: list[int] = []

    while len(user_numbers) < LOTTO_NUMBER_COUNT:
        try:
            raw = input("번호를 입력하세요: ")
            number = int(raw)
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue

        if not is_valid_lotto_number(number, user_numbers):
            print(
                f"잘못된 번호입니다. "
                f"{LOTTO_MIN_NUMBER}~{LOTTO_MAX_NUMBER} 범위, 중복 불가입니다."
            )
            continue

        user_numbers.append(number)

    return user_numbers


def count_match(lotto_numbers: list[int], user_numbers: list[int]) -> int:
    """일치하는 숫자 개수 계산"""
    return len(set(lotto_numbers) & set(user_numbers))


def print_result(lotto_numbers: list[int], user_numbers: list[int], match_count: int):
    """결과 출력 (등수 계산 포함)"""
    print("result:", lotto_numbers)
    print("mine:", user_numbers)

    rank = RANK_BY_MATCH_COUNT.get(match_count, "fail")
    print(rank)


def main() -> None:
    lotto_numbers = generate_lotto_numbers()
    user_numbers = read_user_numbers()
    match_count = count_match(lotto_numbers, user_numbers)
    print_result(lotto_numbers, user_numbers, match_count)


if __name__ == "__main__":
    main()