import random

"""
Comment - Clean Code Principles
주석 작성의 클린 코드 원칙

핵심 메시지:
"주석은 최후의 수단이다.
가장 좋은 주석은 필요 없는 주석이 되도록 코드를 개선하는 것이다."
"""

# ============================================================================
# 나쁜 주석의 종류
# ============================================================================

# ❌ 예시 1 — 불필요한 설명 주석 (코드 그대로 재설명)
# ============================================================================


# Bad: 주석이 코드를 그대로 설명함
def check_lotto_number_bad(number: int) -> bool:
    # 숫자가 1~45 사이인지 검사한다
    if number >= 1 and number <= 45:
        return True
    return False


# 문제점:
# 1. 주석이 "코드 그대로"를 설명함 → 중복
# 2. 코드가 의도를 드러내지 않아서 주석에 의존하게 됨
# 3. 코드가 바뀌면 주석도 수정해야 함 (이중 유지보수)


# Good: 주석 없이 함수명으로 의도를 명확히 표현
def is_in_lotto_range(number: int) -> bool:
    return 1 <= number <= 45


# 사용 예시
number = 30
if is_in_lotto_range(number):
    print(f"{number}는 유효한 로또 번호입니다")


# 개선점:
# ✅ 함수명으로 "주석보다 더 명확하게" 의도가 드러남
# ✅ 주석 제거 → 코드 자체가 주석 역할 수행
# ✅ docstring으로 공식 문서화


# ============================================================================
# ❌ 예시 2 — 감정적/금지성 주석
# ============================================================================


# Bad: 모호하거나 감정적인 주석
def generate_lotto_numbers_bad():
    """
    로또 번호 생성기
    (매우 복잡함, 건들지 마세요)
    """
    # 복잡한 로직이라고만 하고 설명 없음...
    pass


# 문제점:
# ❌ "건들지 마라" 같은 감정적·금지성 주석 → 유지보수 방해
# ❌ 이유 없이 "복잡하다"고만 함 → 아무 도움 안 됨
# ❌ 이런 주석은 레거시 악취


# Good: 구체적이고 건설적인 설명


def generate_lotto_numbers() -> list[int]:
    """
    중복 없는 로또 번호 6개를 생성합니다.

    Returns:
        1~45 범위의 정렬된 숫자 6개
    """
    numbers = random.sample(range(1, 46), 6)
    return sorted(numbers)


# 개선점:
# ✅ 함수가 무엇을 하는지 명확히 설명
# ✅ 감정적 표현 제거
# ✅ 구체적인 동작 설명


# ============================================================================
# ❌ 예시 3 — 주석 처리된 코드 (Dead Code)
# ============================================================================


# Bad: 주석 처리된 코드를 남겨둠
def calculate_score_bad(points: int) -> str:
    result = points * 10
    # old_result = points * 5  # 예전 계산 방식
    # if points > 100:
    #     result = result * 1.5
    # bonus = calculate_bonus(points)  # 보너스 계산 (나중에 추가)
    return f"Score: {result}"


# 문제점:
# ❌ 주석 처리된 코드는 왜 남겨뒀는지 알 수 없음
# ❌ 버전 관리 시스템(Git)이 있으므로 불필요
# ❌ 코드를 지저분하게 만들고 혼란 유발


# Good: 불필요한 코드는 삭제
def calculate_score(points: int) -> str:
    result = points * 10
    return f"Score: {result}"


# 개선점:
# ✅ 주석 처리된 코드 완전 제거
# ✅ Git 히스토리로 과거 코드 추적 가능
# ✅ 깔끔한 코드


# ============================================================================
# ❌ 예시 4 — 오해를 부르는 주석
# ============================================================================


# Bad: 주석과 실제 코드가 다름
def process_user_input(user_input: str) -> int:
    # 사용자 입력을 정수로 변환한다
    try:
        return int(user_input)
    except ValueError:
        return 0  # 실제로는 0을 반환하는데 주석에는 없음


# 문제점:
# ❌ 주석이 예외 처리를 설명하지 않음
# ❌ 코드가 변경되었지만 주석은 업데이트 안 됨
# ❌ 개발자를 오해하게 만듦


# Good: 정확한 docstring
def process_user_input_safe(user_input: str) -> int:
    """
    사용자 입력을 정수로 변환합니다.

    Args:
        user_input: 변환할 문자열

    Returns:
        변환된 정수, 실패 시 0
    """
    try:
        return int(user_input)
    except ValueError:
        return 0


# 개선점:
# ✅ docstring으로 정확한 동작 설명
# ✅ 예외 처리 포함
# ✅ 반환값 명시


# ============================================================================
# ✅ 좋은 주석 예시 1 — 도메인 규칙 설명
# ============================================================================


def calculate_lotto_rank(match_count: int) -> str:
    """
    일치하는 번호 개수로 로또 등수를 계산합니다.

    한국 로또 룰 기준:
    - 6개 일치: 1등
    - 5개 일치: 2등
    - 4개 일치: 3등
    - 3개 일치: 4등
    - 2개 이하: 낙첨 (상금 없음)

    Args:
        match_count: 일치하는 번호 개수

    Returns:
        등수 문자열
    """
    if match_count == 6:
        return "1st"
    if match_count == 5:
        return "2nd"
    if match_count == 4:
        return "3rd"
    if match_count == 3:
        return "4th"
    return "fail"


# 💡 왜 이 주석은 허용될까?
# ✅ "한국 로또 규칙"이라는 도메인 지식은 코드만으로 알 수 없음
# ✅ 변경 가능성이 낮고, 외부 규칙에 대한 설명이므로 유지 가치 있음
# ✅ 비즈니스 로직의 근거를 제공


# ============================================================================
# ✅ 좋은 주석 예시 2 — 법적/비즈니스 관련 강제 규칙
# ============================================================================

# NOTE: 한국 로또 번호 범위는 법적으로 1~45로 고정됨.
# 복권 및 복권기금법 시행령 제9조에 따라 변경 불가.
LOTTO_MIN = 1
LOTTO_MAX = 45

# 💡 이런 주석이 필요한 이유:
# ✅ 법적 근거가 있어서 함부로 변경하면 안 됨
# ✅ "왜 이 값인가?"에 대한 명확한 답변
# ✅ 정책 변경 시 참고할 수 있는 정보


# ============================================================================
# ✅ 좋은 주석 예시 3 — 복잡한 알고리즘 설명
# ============================================================================


def calculate_winning_amount(rank: str, winners_count: int) -> int:
    """
    등수별 당첨금을 계산합니다.

    NOTE: 당첨금 계산 방식
    - 1등: 총 판매액의 75%를 당첨자 수로 균등 분배
    - 2등: 총 판매액의 12.5%를 당첨자 수로 균등 분배
    - 3등: 고정 금액 1,500,000원
    - 4등: 고정 금액 50,000원

    참고: 나눗셈 결과는 천원 단위로 버림 처리
    """
    total_sales = 100_000_000  # 예시 판매액

    if rank == "1st":
        return int(total_sales * 0.75 / winners_count / 1000) * 1000
    elif rank == "2nd":
        return int(total_sales * 0.125 / winners_count / 1000) * 1000
    elif rank == "3rd":
        return 1_500_000
    elif rank == "4th":
        return 50_000
    return 0


# 💡 이 주석이 유용한 이유:
# ✅ 계산 로직의 근거 제공
# ✅ 버림 처리 같은 특수한 규칙 설명
# ✅ 유지보수 시 참고 가능


# ============================================================================
# ✅ 좋은 주석 예시 4 — TODO 주석 모범 사례
# ============================================================================

# TODO는 "임시 보류된 작업"을 추적하는 메모
# ⚠️ 반드시 담당자 + Issue 번호를 함께 적어야 함


# ✅ Good TODO 예시
def format_date_string(date_str: str) -> str:
    """
    날짜 문자열을 파싱합니다.

    TODO(jyami): datetime.utcnow()가 Python 3.12부터 deprecated됨
    이후 datetime.now(timezone.utc)로 교체 필요
    """
    from datetime import datetime

    current_time = datetime.utcnow()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


# ✅ 좋은 TODO의 조건:
# 1. 담당자 명시: TODO(jyami)
# 2. 구체적인 작업 내용: "deprecated 메서드를 새 메서드로 교체"
# 3. 이유 설명: "라이브러리 업데이트로 인한 deprecated"
# 4. Issue 번호: #42
# 5. 참고 문서: PEP 또는 공식 문서 링크
# 6. 예상 시점: "Python 3.14 릴리즈 후"


# ❌ Bad TODO 예시
def bad_todo_example():
    # TODO: 고쳐야 함
    # TODO: 나중에 수정
    # TODO: 이거 이상한데
    pass


# 나쁜 TODO의 문제점:
# ❌ 누가 고치는지 모름
# ❌ 언제까지 해야하는지 모름
# ❌ 어떤 문제인지 모름
# ❌ "고쳐야 한다"는 감정만 남음 (아무 의미 없음)


# ============================================================================
# ✅ 좋은 주석 예시 5 — FIXME, HACK, XXX 등의 마커
# ============================================================================


def process_data(data: list[int]) -> list[int]:
    """데이터를 처리합니다."""

    # FIXME(jyami): 빈 리스트 처리 시 에러 발생
    # Issue: #123
    # 재현: process_data([]) 호출 시 IndexError
    if not data:
        return []

    # HACK(jyami): 임시 해결책 - 성능 최적화 필요
    # 현재 O(n²) 알고리즘, O(n log n)으로 개선 예정
    # 데이터가 10,000개 이상일 때 느려짐
    result = []
    for item in data:
        if item not in result:
            result.append(item)

    return result


# 주석 마커 종류:
# - TODO: 나중에 해야 할 작업
# - FIXME: 알려진 버그, 반드시 수정 필요
# - HACK: 임시 해결책, 더 나은 방법 필요
# - XXX: 위험하거나 문제가 있는 코드
# - NOTE: 중요한 설명이나 참고 사항


# ============================================================================
# Before/After 종합 예제 — 주석이 많은 코드 → 주석이 필요 없는 코드
# ============================================================================


# ❌ Before: 주석 투성이 코드
def calculate_price_bad(price, count, is_member):
    # 가격을 계산한다
    total = price * count

    # 회원이면 할인을 적용한다
    if is_member:
        # 10% 할인
        discount = total * 0.1
        # 총액에서 할인액을 뺀다
        total = total - discount

    # 최종 가격을 반환한다
    return total


# ✅ After: 주석 없이 의도가 명확한 코드
MEMBER_DISCOUNT_RATE = 0.1


def calculate_total_price(price: int, count: int) -> int:
    """총 가격을 계산합니다."""
    return price * count


def apply_member_discount(total: int) -> int:
    """회원 할인을 적용합니다."""
    discount = total * MEMBER_DISCOUNT_RATE
    return total - discount


def calculate_price(price: int, count: int, is_member: bool) -> int:
    """
    최종 가격을 계산합니다.

    Args:
        price: 단가
        count: 수량
        is_member: 회원 여부

    Returns:
        할인이 적용된 최종 가격
    """
    total = calculate_total_price(price, count)

    if is_member:
        total = apply_member_discount(total)

    return total


# 개선점:
# ✅ 주석을 함수로 대체 (calculate_total_price, apply_member_discount)
# ✅ 상수로 매직 넘버 제거 (MEMBER_DISCOUNT_RATE)
# ✅ 타입 힌트로 명확성 향상
# ✅ docstring으로 공식 문서화
# ✅ 코드 자체가 주석 역할 수행


# ============================================================================
# 정리: 주석 작성 체크리스트
# ============================================================================

"""
❌ 나쁜 주석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✗ 코드 그대로 재설명
✗ 감정적, 금지성, 부정확한 정보
✗ 주석 처리된 코드 (Dead Code)
✗ TODO가 불명확한 경우 (담당자·이유·기한 없음)
✗ 오해를 부르거나 잘못된 정보

✅ 좋은 주석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 코드만으로 알 수 없는 정보
✓ 도메인 규칙 / 외부 시스템 설명
✓ 법적·정책적 제약
✓ 복잡한 알고리즘의 근거
✓ TODO + 담당자 + Issue 번호 + 이유
✓ FIXME, HACK 등으로 문제점 명확히 표시

💡 황금 원칙
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"주석이 필요하다면, 먼저 코드를 개선할 방법을 찾아라.
주석은 최후의 수단이다."

1. 주석을 쓰기 전에: 함수로 추출할 수 있는가?
2. 주석을 쓰기 전에: 변수명/함수명을 개선할 수 있는가?
3. 주석을 쓰기 전에: 상수로 만들 수 있는가?
4. 그래도 필요하다면: docstring이나 명확한 주석을 작성하라
"""


if __name__ == "__main__":
    print("=== 주석 작성 클린 코드 원칙 ===\n")

    # 예제 실행
    print("1. 로또 번호 범위 확인")
    print(f"   30은 유효? {is_in_lotto_range(30)}")
    print(f"   50은 유효? {is_in_lotto_range(50)}\n")

    print("2. 로또 번호 생성")
    numbers = generate_lotto_numbers()
    print(f"   생성된 번호: {numbers}\n")

    print("3. 로또 등수 계산")
    print(f"   6개 일치: {calculate_lotto_rank(6)}")
    print(f"   3개 일치: {calculate_lotto_rank(3)}")
    print(f"   1개 일치: {calculate_lotto_rank(1)}\n")

    print("4. 가격 계산 (Before/After)")
    print(f"   회원 가격: {calculate_price(10000, 3, True):,}원")
    print(f"   비회원 가격: {calculate_price(10000, 3, False):,}원")
