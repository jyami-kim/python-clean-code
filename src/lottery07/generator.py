import random
from typing import Callable, Protocol

from src.lottery07.const import LOTTO_MAX_NUMBER, LOTTO_MIN_NUMBER, LOTTO_NUMBER_COUNT
from src.lottery07.model import LottoNumbers


class LottoGenerator(Protocol):
    def generate(self) -> LottoNumbers: ...


class AutoLottoGenerator:
    def generate(self) -> LottoNumbers:
        numbers: list[int] = []
        while len(numbers) < LOTTO_NUMBER_COUNT:
            candidate = random.randint(LOTTO_MIN_NUMBER, LOTTO_MAX_NUMBER)
            if candidate in numbers:
                continue
            numbers.append(candidate)

        return LottoNumbers(numbers=numbers)


class FixedLottoGenerator:
    def __init__(self, fixed_numbers: list[int]) -> None:
        self.lotto_numbers = LottoNumbers(numbers=fixed_numbers)

    def generate(self) -> LottoNumbers:
        return self.lotto_numbers


class ManualLottoGenerator:
    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        print_func: Callable[[str], None] = print,
    ) -> None:
        self.input_func = input_func
        self.print_func = print_func

    def generate(self) -> LottoNumbers:
        numbers: list[int] = []

        while len(numbers) < LOTTO_NUMBER_COUNT:
            remaining = LOTTO_NUMBER_COUNT - len(numbers)
            raw = self.input_func(
                f"번호를 입력하세요 (남은 개수: {remaining}개, 범위: {LOTTO_MIN_NUMBER}~{LOTTO_MAX_NUMBER}): "
            )

            try:
                number = int(raw)
            except ValueError:
                self.print_func("숫자를 입력해 주세요.")
                continue

            if not (LOTTO_MIN_NUMBER <= number <= LOTTO_MAX_NUMBER):
                self.print_func(f"{LOTTO_MIN_NUMBER}~{LOTTO_MAX_NUMBER} 범위만 허용됩니다.")
                continue

            if number in numbers:
                self.print_func("중복된 번호입니다.")
                continue

            numbers.append(number)
            self.print_func(f"{number} 추가됨 (현재: {numbers})")

        return LottoNumbers(numbers=numbers)
