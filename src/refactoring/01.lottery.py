import random

lotto_numbers = []
for _ in range(6):
    candidate = random.randint(1, 45)
    while candidate in lotto_numbers:
        candidate = random.randint(1, 45)
    lotto_numbers.append(candidate)

user_numbers = []
for _ in range(6):
    number = int(input("번호를 입력하세요: "))
    while number < 1 or number > 45 or number in user_numbers:
        print("잘못된 번호입니다.")
        number = int(input("번호를 다시 입력하세요: "))
    user_numbers.append(number)

match_count = 0
for number in lotto_numbers:
    if number in user_numbers:
        match_count += 1

print("result:", lotto_numbers)
print("mine:", user_numbers)
if match_count == 6:
    print("1st")
elif match_count == 5:
    print("2nd")
elif match_count == 4:
    print("3rd")
elif match_count == 3:
    print("4th")
else:
    print("fail")

