"""
lottery07 생성 전략 테스트
Strategy Pattern for Lotto Generator
"""

from unittest.mock import Mock

import pytest

from src.lottery07.generator import (
    AutoLottoGenerator,
    FixedLottoGenerator,
    ManualLottoGenerator,
)
from src.lottery07.model import LottoNumbers


class TestAutoLottoGenerator:
    """자동 생성 전략 테스트"""

    def test_generate_returns_lotto_numbers(self):
        """생성된 번호는 LottoNumbers 모델"""
        generator = AutoLottoGenerator()
        result = generator.generate()

        assert isinstance(result, LottoNumbers)

    def test_generate_returns_6_unique_numbers(self):
        """6개의 중복 없는 번호 생성"""
        generator = AutoLottoGenerator()
        result = generator.generate()

        assert len(result.numbers) == 6
        assert len(set(result.numbers)) == 6

    def test_generate_numbers_in_valid_range(self):
        """1~45 범위의 번호 생성"""
        generator = AutoLottoGenerator()
        result = generator.generate()

        assert all(1 <= num <= 45 for num in result.numbers)

    def test_generate_multiple_times(self):
        """여러 번 생성해도 항상 유효"""
        generator = AutoLottoGenerator()

        for _ in range(10):
            result = generator.generate()
            assert isinstance(result, LottoNumbers)
            assert len(result.numbers) == 6


class TestFixedLottoGenerator:
    """고정 생성 전략 테스트 (테스트용)"""

    def test_generate_returns_fixed_numbers(self):
        """항상 동일한 번호 반환"""
        fixed_numbers = [1, 10, 20, 30, 40, 45]
        generator = FixedLottoGenerator(fixed_numbers)

        result = generator.generate()
        assert result.numbers == fixed_numbers

    def test_generate_multiple_times_same_result(self):
        """여러 번 생성해도 동일한 결과"""
        fixed_numbers = [5, 15, 25, 35, 40, 45]
        generator = FixedLottoGenerator(fixed_numbers)

        result1 = generator.generate()
        result2 = generator.generate()
        result3 = generator.generate()

        assert result1.numbers == result2.numbers == result3.numbers == fixed_numbers

    def test_invalid_fixed_numbers_raises_error(self):
        """유효하지 않은 번호로 생성 시 에러"""
        from pydantic import ValidationError

        # 개수 부족
        with pytest.raises(ValidationError):
            FixedLottoGenerator([1, 10, 20])

        # 범위 초과
        with pytest.raises(ValidationError):
            FixedLottoGenerator([1, 10, 20, 30, 40, 50])

        # 중복
        with pytest.raises(ValidationError):
            FixedLottoGenerator([1, 1, 20, 30, 40, 45])


class TestManualLottoGenerator:
    """수동 입력 전략 테스트"""

    def test_generate_with_valid_inputs(self):
        """유효한 입력으로 번호 생성"""
        mock_input = Mock(side_effect=["1", "10", "20", "30", "40", "45"])
        mock_print = Mock()

        generator = ManualLottoGenerator(input_func=mock_input, print_func=mock_print)
        result = generator.generate()

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        assert mock_input.call_count == 6

    def test_generate_retry_on_non_numeric(self):
        """숫자가 아닌 입력 시 재시도"""
        mock_input = Mock(side_effect=["abc", "1", "10", "20", "30", "40", "45"])
        mock_print = Mock()

        generator = ManualLottoGenerator(input_func=mock_input, print_func=mock_print)
        result = generator.generate()

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        assert mock_input.call_count == 7
        mock_print.assert_any_call("숫자를 입력해 주세요.")

    def test_generate_retry_on_out_of_range(self):
        """범위 밖 입력 시 재시도"""
        mock_input = Mock(side_effect=["0", "1", "10", "20", "30", "40", "45"])
        mock_print = Mock()

        generator = ManualLottoGenerator(input_func=mock_input, print_func=mock_print)
        result = generator.generate()

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        mock_print.assert_any_call("1~45 범위만 허용됩니다.")

    def test_generate_retry_on_duplicate(self):
        """중복 입력 시 재시도"""
        mock_input = Mock(side_effect=["1", "1", "10", "20", "30", "40", "45"])
        mock_print = Mock()

        generator = ManualLottoGenerator(input_func=mock_input, print_func=mock_print)
        result = generator.generate()

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        mock_print.assert_any_call("중복된 번호입니다.")

    def test_generate_shows_progress(self):
        """입력 진행 상황 표시"""
        mock_input = Mock(side_effect=["1", "10", "20", "30", "40", "45"])
        mock_print = Mock()

        generator = ManualLottoGenerator(input_func=mock_input, print_func=mock_print)
        generator.generate()

        # 각 번호가 추가될 때마다 진행 상황 출력
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("추가됨" in str(call) for call in calls)


class TestGeneratorStrategy:
    """생성 전략 교체 테스트 (Strategy Pattern)"""

    def test_strategy_can_be_swapped(self):
        """생성 전략을 자유롭게 교체 가능"""

        def use_generator(generator) -> LottoNumbers:
            """생성 전략을 주입받아 실행"""
            return generator.generate()

        # 자동 생성 전략
        auto_gen = AutoLottoGenerator()
        auto_result = use_generator(auto_gen)
        assert isinstance(auto_result, LottoNumbers)

        # 고정 생성 전략
        fixed_gen = FixedLottoGenerator([1, 2, 3, 4, 5, 6])
        fixed_result = use_generator(fixed_gen)
        assert fixed_result.numbers == [1, 2, 3, 4, 5, 6]

        # 수동 생성 전략
        mock_input = Mock(side_effect=["10", "20", "30", "40", "41", "42"])
        manual_gen = ManualLottoGenerator(input_func=mock_input, print_func=Mock())
        manual_result = use_generator(manual_gen)
        assert manual_result.numbers == [10, 20, 30, 40, 41, 42]

    def test_all_generators_follow_same_interface(self):
        """모든 Generator는 동일한 인터페이스 준수"""
        generators = [
            AutoLottoGenerator(),
            FixedLottoGenerator([1, 10, 20, 30, 40, 45]),
            ManualLottoGenerator(
                input_func=Mock(side_effect=["1", "10", "20", "30", "40", "45"]),
                print_func=Mock(),
            ),
        ]

        for generator in generators:
            # 모든 Generator는 generate() 메서드를 가짐
            assert hasattr(generator, "generate")
            assert callable(generator.generate)

            # generate() 결과는 LottoNumbers 모델
            result = generator.generate()
            assert isinstance(result, LottoNumbers)
