"""
Variable Naming - Clean Code Principles
변수명 작성의 클린 코드 원칙들을 보여주는 예제
"""

# ============================================================================
# 1. 의도를 분명히 밝혀라 (Reveal Your Intention)
# ============================================================================

# Bad: 의미를 알 수 없는 변수명
d = 10  # 아마도 duration?
t = 86400  # 아마도 시간?

# Good: 의도가 명확한 변수명
elapsed_days = 10
seconds_per_day = 86400


# ============================================================================
# 2. 그릇된 정보를 피하라 (Avoid Disinformation)
# ============================================================================

# Bad: 실제로는 리스트가 아닌데 list라는 이름 사용
account_list = {"user1": 1000, "user2": 2000}  # 실제로는 dict

# Good: 정확한 타입을 나타내는 이름
account_dict = {"user1": 1000, "user2": 2000}
account_group = {"user1": 1000, "user2": 2000}


# Bad: 비슷한 이름으로 혼동 유발
XYZControllerForEfficientHandlingOfStrings = "controller1"
XYZControllerForEfficientStorageOfStrings = "controller2"

# Good: 명확하게 구분되는 이름
string_handler = "controller1"
string_storage = "controller2"


# ============================================================================
# 3. 의미 있게 구분하라 (Make Meaningful Distinctions)
# ============================================================================

# Bad: 숫자로만 구분
def copy_chars(a1: str, a2: str):
    for i in range(len(a1)):
        a2 += a1[i]

# Good: 의미 있는 이름으로 구분
def copy_chars(source: str, destination: str):
    for char in source:
        destination += char


# Bad: 불용어(noise words) 사용
def get_product_info():
    return "laptop"
def get_product_data ():
    return "laptop"
def get_product ():
    return "laptop"

def get_name_string():
    return "Name"
def get_name():
    return "Name"

def get_customer():
    return Customer()
def get_customer_object():
    return Customer()

# Good: 명확한 차이가 있는 이름
product_name = "laptop"
product_price = 1000
product_inventory = 50

class Customer:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id    


# ============================================================================
# 4. 발음하기 쉬운 이름을 사용하라 (Use Pronounceable Names)
# ============================================================================

# Bad: 발음하기 어렵고 의미 파악이 어려움
genymdhms = "20231215143022"  # generation year/month/day/hour/minute/second
modymdhms = "20231216091505"

# Good: 발음 가능하고 의미가 명확함
generation_timestamp = "20231215143022"
modification_timestamp = "20231216091505"


# ============================================================================
# 5. 검색하기 쉬운 이름을 사용하라 (Use Searchable Names)
# ============================================================================

# Bad: 매직 넘버 사용
for i in range(5):
    print(f"Day {i}")

# Good: 상수로 정의하여 검색 가능하게
WORK_DAYS_PER_WEEK = 5
for day in range(WORK_DAYS_PER_WEEK):
    print(f"Day {day}")


# Bad: 한 글자 변수명 (검색 어려움)
s = 0
for t in range(34):
    s += (t + 3) * 5

# Good: 의미 있는 변수명
sum_of_tasks = 0
number_of_tasks = 34
for task_index in range(number_of_tasks):
    sum_of_tasks += (task_index + 3) * 5


# ============================================================================
# 6. 인코딩을 피하라 (Avoid Encodings)
# ============================================================================

# Bad: 헝가리안 표기법 (타입을 변수명에 포함)
str_name = "John"
int_age = 30
list_items = [1, 2, 3]

# Good: 타입 힌트 사용 (Python 3.5+)
name: str = "John"
age: int = 30
items: list[int] = [1, 2, 3]

# 💡 타입 힌트의 장점은 02.type_hint.py에서 자세히 다룹니다

# Bad: 멤버 변수 접두사 (m_)
class Person:
    def __init__(self):
        self.m_name = "John"  # 불필요한 접두사
        self.m_age = 30

# Good: 간결하고 명확한 이름
class Person:
    def __init__(self):
        self.name = "John"
        self.age = 30


# ============================================================================
# 7. 자신의 기억력을 자랑하지 마라 (Avoid Mental Mapping)
# ============================================================================

# Bad: 루프 변수를 다른 용도로 사용
for i in range(10):
    # i를 user_id처럼 사용
    print(f"Processing user {i}")

# Good: 명확한 변수명 사용
for user_id in range(10):
    print(f"Processing user {user_id}")


# ============================================================================
# 8. 클래스 이름 (Class Names)
# ============================================================================

# Bad: 동사나 Manager, Processor 같은 모호한 이름
class Manager:
    pass

class Data:
    pass

# Good: 명사나 명사구 사용
class Customer:
    pass

class Account:
    pass

class AddressParser:
    pass


# ============================================================================
# 9. 메서드 이름 (Method Names)
# ============================================================================

# Bad: 모호한 동사
class UserAccount:
    def do(self):
        pass
    
    def process(self):
        pass

# Good: 명확한 동사 사용
class UserAccount:
    def create_account(self):
        pass
    
    def delete_account(self):
        pass
    
    def get_balance(self) -> float:
        return 0.0
    
    def is_active(self) -> bool:
        return True


# ============================================================================
# 10. 기발한 이름은 피하라 (Don't Be Cute)
# ============================================================================

# Bad: 재치있지만 불명확한 이름
def holyHandGrenade():  # 삭제 함수를 의미
    pass

def whack():  # 종료 함수를 의미
    pass

# Good: 직관적이고 명확한 이름
def delete_items():
    pass

def terminate_process():
    pass


# ============================================================================
# 11. 한 개념에 한 단어를 사용하라 (Pick One Word per Concept)
# ============================================================================

# Bad: 같은 개념에 다른 단어 사용
class UserController:
    def fetch_user(self):
        pass

class OrderController:
    def retrieve_order(self):
        pass

class ProductController:
    def get_product(self):
        pass

# Good: 일관된 단어 사용
class UserController:
    def get_user(self):
        pass

class OrderController:
    def get_order(self):
        pass

class ProductController:
    def get_product(self):
        pass


# ============================================================================
# 12. 해법 영역과 문제 영역의 이름 (Use Solution/Problem Domain Names)
# ============================================================================

# Good: 기술 개념은 기술 용어 사용
class AccountVisitor:  # Visitor 패턴
    pass

class JobQueue:  # Queue 자료구조
    pass

# Good: 비즈니스 로직은 도메인 용어 사용
class PolicyCalculator:  # 보험 도메인
    pass

class LoanApproval:  # 금융 도메인
    pass


# ============================================================================
# 13. 의미 있는 맥락을 추가하라 (Add Meaningful Context)
# ============================================================================

# Bad: 맥락이 불분명한 변수
first_name = "John"
last_name = "Doe"
state = "CA"
city = "Los Angeles"
street = "Main St"
house_number = "123"

# Good: 클래스로 맥락 부여
class Address:
    def __init__(self):
        self.state = "CA"
        self.city = "Los Angeles"
        self.street = "Main St"
        self.house_number = "123"

# Good: 접두사로 맥락 부여 (클래스가 과할 때)
address_state = "CA"
address_city = "Los Angeles"
address_street = "Main St"
address_house_number = "123"
