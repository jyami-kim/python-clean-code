import random

# 매직 넘버를 의미 있는 상수로 분리
LOTTO_NUMBER_COUNT = 6
LOTTO_MIN_NUMBER = 1
LOTTO_MAX_NUMBER = 45

RANK_BY_MATCH_COUNT = {
    6: "1st",
    5: "2nd",
    4: "3rd",
    3: "4th",
}

lotto_numbers = []
for _ in range(LOTTO_NUMBER_COUNT):
    candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
    while candidate in lotto_numbers:
        candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
    lotto_numbers.append(candidate)

user_numbers = []
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

match_count = 0
for number in lotto_numbers:
    if number in user_numbers:
        match_count += 1

print("result:", lotto_numbers)
print("mine:", user_numbers)

# ✅ 등수도 매직 넘버 대신 매핑 사용
rank = RANK_BY_MATCH_COUNT.get(match_count, "fail")
print(rank)