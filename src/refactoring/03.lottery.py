import random

# 상수 분리 (매직 넘버 제거)
LOTTO_NUMBER_COUNT = 6
LOTTO_MIN_NUMBER = 1
LOTTO_MAX_NUMBER = 45

RANK_BY_MATCH_COUNT = {
    6: "1st",
    5: "2nd",
    4: "3rd",
    3: "4th",
}

def generate_lotto_numbers() -> list[int]:
    """로또 번호 6개 생성"""
    lotto_numbers: list[int] = []
    for _ in range(LOTTO_NUMBER_COUNT):
        candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
        while candidate in lotto_numbers:
            candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
        lotto_numbers.append(candidate)
    return lotto_numbers


def read_user_numbers() -> list[int]:
    """사용자 번호 입력 + 검증"""
    user_numbers: list[int] = []
    for _ in range(LOTTO_NUMBER_COUNT):
        number = int(input("번호를 입력하세요: "))
        while (
            number < LOTTO_MIN_NUMBER
            or number > LOTTO_MAX_NUMBER
            or number in user_numbers
        ):
            print("잘못된 번호입니다.")
            number = int(input("번호를 다시 입력하세요: "))
        user_numbers.append(number)
    return user_numbers


def count_match(lotto_numbers: list[int], user_numbers: list[int]) -> int:
    """일치하는 숫자 개수 계산"""
    match_count = 0
    for number in lotto_numbers:
        if number in user_numbers:
            match_count += 1
    return match_count


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