"""
Type Hints - Why Python Developers Should Use Type Hints
타입 힌트 - 왜 Python 개발자가 타입 힌트를 사용해야 하는가?
"""

# ============================================================================
# 헝가리안 표기법 vs 타입 힌트
# ============================================================================

# Bad: 헝가리안 표기법 (타입을 변수명에 포함)
str_name = "John"
int_age = 30
list_items = [1, 2, 3]
dict_user_info = {"name": "John", "age": 30}

# Good: 타입 힌트 사용 (Python 3.5+)
name: str = "John"
age: int = 30
items: list[int] = [1, 2, 3]
user_info: dict[str, str | int] = {"name": "John", "age": 30}


# ============================================================================
# 1. 팀 협업에서 함수의 의도가 선명해짐
# ============================================================================
"""
✅ "이 함수는 무엇을 받고, 무엇을 반환하는가"가 명료화
✅ 함수 시그니처 자체가 "계약(contract)" 역할
"""

# Bad: 함수 시그니처만으로는 무엇을 받고 반환하는지 불명확
def calculate_discount(price, rate, is_member):
    """할인된 가격을 계산합니다."""
    if is_member:
        return price * (1 - rate)
    return price * (1 - rate * 0.5)

# 문제점:
# - price가 int인가 float인가?
# - rate는 0.0~1.0인가 0~100인가?
# - is_member가 bool인가 string인가?
# - 반환값은 무엇인가?


# Good: 타입 힌트로 "계약(contract)"이 명확해짐
def calculate_discount_typed(
    price: float, 
    rate: float, 
    is_member: bool
) -> float:
    """
    할인된 가격을 계산합니다.
    
    Args:
        price: 원가 (양수)
        rate: 할인율 (0.0 ~ 1.0)
        is_member: 회원 여부
    
    Returns:
        할인된 최종 가격
    """
    if is_member:
        return price * (1 - rate)
    return price * (1 - rate * 0.5)

# 장점:
# - 함수 시그니처만 봐도 입출력이 명확
# - 팀원이 함수 구현을 보지 않아도 사용 가능
# - 코드 리뷰 시간 단축


# ============================================================================
# 2. 대규모 프로젝트에서 리팩토링 안정성 급증
# ============================================================================
"""
✅ 잘못된 타입 변경을 정적 분석기로 즉시 발견 가능
✅ 수백 개의 파일이 있어도 안전하게 리팩토링
"""

# Bad: 타입 변경 시 어디서 문제가 생길지 찾기 어려움
def process_user_data(data):
    # data가 dict인지, list인지, 뭔지 모름
    return data.get("name", "Unknown")  # 런타임에 AttributeError 발생 가능

# 만약 data가 list로 변경되면?
# → 런타임에 가서야 에러 발견 (프로덕션에서 장애 가능)


# Good: 정적 분석기(mypy, pyright)가 타입 오류를 즉시 발견
def process_user_data_typed(data: dict[str, str]) -> str:
    return data.get("name", "Unknown")  # IDE가 자동완성 제공, 타입 체커가 검증

# 만약 data 타입을 list[str]로 변경하면?
# → mypy/pyright가 즉시 "dict.get() 메서드가 없다"고 에러 표시
# → 코드 작성 시점에 문제 발견 및 수정


# 실제 리팩토링 시나리오
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

def get_user_name(user: User) -> str:
    return user.name

def get_user_id(user: User) -> int:
    return user.user_id

def send_email(user: User, message: str) -> None:
    print(f"Sending to {user.email}: {message}")

# User 클래스의 email 필드를 email_address로 변경하면?
# → 타입 체커가 send_email() 함수에서 에러 표시
# → 관련된 모든 코드를 안전하게 수정 가능


# ============================================================================
# 3. IDE 자동완성이 정확해짐 → 생산성 + 버그 감소
# ============================================================================
"""
✅ IDE가 정확한 자동완성 제공
✅ 타이핑 속도 향상 + 오타 방지
✅ 메서드/속성 탐색 시간 제로
"""

from typing import Optional

class Customer:
    def __init__(self, name: str, email: str, phone: Optional[str] = None):
        self.name = name
        self.email = email
        self.phone = phone
    
    def get_contact_info(self) -> str:
        return f"{self.name} <{self.email}>"
    
    def has_phone(self) -> bool:
        return self.phone is not None


# Bad: IDE가 customer의 메서드를 알 수 없음
def send_notification(customer):
    # customer. 입력 시:
    # - 자동완성 안됨
    # - 메서드 이름을 기억해야 함
    # - 오타 가능성 높음
    print(f"Sending to {customer.email}")

# Good: IDE가 정확한 자동완성 제공
def send_notification_typed(customer: Customer) -> None:
    # customer. 입력 시:
    # - name, email, phone 자동완성
    # - get_contact_info(), has_phone() 메서드 자동완성
    # - 각 메서드의 반환 타입도 표시
    contact = customer.get_contact_info()  # IDE가 반환 타입(str)도 알려줌
    print(f"Sending to {contact}")
    
    if customer.has_phone():  # IDE가 반환 타입(bool)을 알고 있음
        print(f"Phone: {customer.phone}")


# ============================================================================
# 4. 문서 역할 (Self-Documenting Code)
# ============================================================================
"""
✅ Docstring보다 더 정확한 "계약 정보(contract)" 제공
✅ 코드 자체가 문서 역할
✅ 문서와 코드의 불일치 방지
"""

from typing import List, Dict, Tuple
from datetime import datetime

# Bad: Docstring만으로는 정확한 타입 정보 부족
def analyze_sales_data(data, start, end):
    """
    매출 데이터를 분석합니다.
    
    Args:
        data: 매출 데이터 (리스트? 딕셔너리?)
        start: 시작일 (문자열? datetime?)
        end: 종료일 (문자열? datetime?)
    
    Returns:
        분석 결과 (무엇을? 어떤 형태로?)
    """
    pass

# 문제점:
# - 타입이 모호함
# - Docstring이 업데이트 안 될 수 있음
# - 실제 구현과 문서가 불일치 가능


# Good: 타입 힌트가 정확한 "계약 정보(contract)" 제공
def analyze_sales_data_typed(
    data: List[Dict[str, float]],
    start: datetime,
    end: datetime
) -> Tuple[float, float, Dict[str, float]]:
    """
    매출 데이터를 분석합니다.
    
    Args:
        data: 날짜별 매출 데이터 리스트
        start: 분석 시작일
        end: 분석 종료일
    
    Returns:
        (총 매출, 평균 매출, 카테고리별 매출) 튜플
    """
    total_sales = sum(item["amount"] for item in data)
    avg_sales = total_sales / len(data) if data else 0.0
    category_sales = {"electronics": 1000.0, "clothing": 500.0}
    
    return total_sales, avg_sales, category_sales

# 장점:
# - 타입 힌트가 항상 정확함 (코드와 분리될 수 없음)
# - IDE가 타입을 기반으로 자동완성 제공
# - 타입 체커가 검증해줌


# ============================================================================
# 5. 복잡한 타입도 명확하게 표현 가능
# ============================================================================
"""
✅ 제네릭, 유니온, 타입 별칭 등으로 복잡한 타입 표현
✅ 도메인 개념을 타입으로 표현
"""

from typing import Union, Callable, TypeAlias, Literal

# 타입 별칭으로 복잡한 타입을 의미있게 표현
UserId: TypeAlias = int
UserName: TypeAlias = str
Email: TypeAlias = str
UserData: TypeAlias = Dict[str, Union[str, int, bool]]
ValidationFunc: TypeAlias = Callable[[UserData], bool]

# Literal 타입으로 가능한 값 제한
UserRole = Literal["admin", "user", "guest"]
Status = Literal["pending", "approved", "rejected"]

def create_user(
    name: UserName,
    email: Email,
    role: UserRole = "user"
) -> UserId:
    """
    새 사용자를 생성합니다.
    
    Args:
        name: 사용자 이름
        email: 이메일 주소
        role: 사용자 역할 (admin, user, guest 중 하나)
    
    Returns:
        생성된 사용자 ID
    """
    # 실제 구현...
    return 12345

def validate_user(
    user_data: UserData,
    validators: List[ValidationFunc]
) -> Tuple[bool, List[str]]:
    """
    사용자 데이터를 검증합니다.
    
    Args:
        user_data: 검증할 사용자 데이터
        validators: 검증 함수 리스트
    
    Returns:
        (검증 성공 여부, 에러 메시지 리스트)
    """
    errors = []
    for validator in validators:
        if not validator(user_data):
            errors.append("Validation failed")
    
    return len(errors) == 0, errors


# ============================================================================
# 6. 실전 예제: 온라인 쇼핑몰
# ============================================================================

from typing import Protocol
from decimal import Decimal

# Protocol을 사용한 덕 타이핑
class Discountable(Protocol):
    """할인 가능한 객체의 인터페이스"""
    def get_price(self) -> Decimal: ...
    def apply_discount(self, rate: float) -> Decimal: ...

class Product:
    def __init__(self, name: str, price: Decimal, stock: int):
        self.name = name
        self.price = price
        self.stock = stock
    
    def get_price(self) -> Decimal:
        return self.price
    
    def apply_discount(self, rate: float) -> Decimal:
        return self.price * Decimal(1 - rate)
    
    def is_in_stock(self) -> bool:
        return self.stock > 0

class Cart:
    def __init__(self):
        self.items: List[Tuple[Product, int]] = []
    
    def add_item(self, product: Product, quantity: int = 1) -> None:
        """
        장바구니에 상품을 추가합니다.
        
        Args:
            product: 추가할 상품
            quantity: 수량 (기본값: 1)
        """
        self.items.append((product, quantity))
    
    def calculate_total(self, discount_rate: float = 0.0) -> Decimal:
        """
        장바구니의 총 금액을 계산합니다.
        
        Args:
            discount_rate: 할인율 (0.0 ~ 1.0)
        
        Returns:
            총 금액
        """
        total = Decimal(0)
        for product, quantity in self.items:
            if discount_rate > 0:
                price = product.apply_discount(discount_rate)
            else:
                price = product.get_price()
            total += price * quantity
        return total
    
    def get_items(self) -> List[Tuple[Product, int]]:
        """장바구니의 모든 상품을 반환합니다."""
        return self.items.copy()


# ============================================================================
# 타입 힌트 vs 헝가리안 표기법 비교 요약
# ============================================================================

"""
헝가리안 표기법의 문제점:
❌ 변수명이 길어지고 가독성 저하
   예: str_user_name, list_product_items, dict_user_profile
   
❌ 타입 변경 시 변수명도 일일이 변경해야 함
   예: list_users → set_users (모든 코드에서 변경 필요)
   
❌ IDE와 정적 분석 도구의 도움을 받을 수 없음
   → 자동완성, 타입 체크 불가능
   
❌ 복잡한 타입(제네릭, 유니온 등)을 표현하기 어려움
   예: dict[str, list[tuple[int, str]]] → ??? (표현 불가)

타입 힌트의 장점:
✅ 변수명은 간결하게, 타입 정보는 별도로 명시
   예: users: list[User] (변수명은 간결, 타입은 정확)
   
✅ 타입 변경 시 타입 힌트만 수정하면 됨
   예: users: list[User] → users: set[User] (변수명 유지)
   
✅ IDE 자동완성, 타입 체커(mypy, pyright)의 지원
   → 개발 생산성 대폭 향상
   
✅ 복잡한 타입도 정확하게 표현 가능
   예: Dict[str, List[Tuple[int, str, Optional[float]]]]
   
✅ 문서화 효과 + 리팩토링 안정성 제공
   → 코드 자체가 문서 + 안전한 리팩토링
   
✅ 팀 협업 시 "계약(contract)" 역할로 의사소통 개선
   → 함수 시그니처만으로 사용법 이해
"""


# ============================================================================
# 실습: 타입 힌트 적용해보기
# ============================================================================

if __name__ == "__main__":
    print("=== 타입 힌트 데모 ===\n")
    
    # 1. 할인 계산
    original_price = 10000.0
    discount_rate = 0.2
    is_member = True
    
    final_price = calculate_discount_typed(original_price, discount_rate, is_member)
    print(f"원가: {original_price}원")
    print(f"할인율: {discount_rate * 100}%")
    print(f"회원: {'예' if is_member else '아니오'}")
    print(f"최종 가격: {final_price}원\n")
    
    # 2. 쇼핑몰 예제
    product1 = Product("노트북", Decimal("1000000"), 10)
    product2 = Product("마우스", Decimal("30000"), 50)
    
    cart = Cart()
    cart.add_item(product1, 1)
    cart.add_item(product2, 2)
    
    total = cart.calculate_total()
    total_with_discount = cart.calculate_total(0.1)
    
    print("장바구니:")
    for product, quantity in cart.get_items():
        print(f"  - {product.name}: {product.get_price()}원 x {quantity}개")
    
    print(f"\n총액: {total}원")
    print(f"10% 할인 적용: {total_with_discount}원")
    print(f"절감액: {total - total_with_discount}원")
