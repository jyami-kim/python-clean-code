from unittest.mock import patch

from src.lottery04 import (
    is_valid_lotto_number,
    generate_lotto_numbers,
    read_user_numbers,
    count_match,
    print_result,
    LOTTO_NUMBER_COUNT,
    LOTTO_MIN_NUMBER,
    LOTTO_MAX_NUMBER,
)


class TestIsValidLottoNumber:
    """로또 번호 유효성 검증 테스트"""
    
    def test_valid_number_within_range(self):
        """유효한 범위 내의 번호는 True를 반환한다"""
        assert is_valid_lotto_number(25, [1, 2, 3]) is True

    def test_number_below_min_range(self):
        """최소값보다 작은 번호는 False를 반환한다"""
        assert is_valid_lotto_number(0, [1, 2, 3]) is False

    def test_number_above_max_range(self):
        """최대값보다 큰 번호는 False를 반환한다"""
        assert is_valid_lotto_number(46, [1, 2, 3]) is False

    def test_duplicate_number(self):
        """중복된 번호는 False를 반환한다"""
        assert is_valid_lotto_number(2, [1, 2, 3]) is False

    def test_min_boundary(self):
        """최소값(1)은 유효한 번호다"""
        assert is_valid_lotto_number(1, [2, 3, 4]) is True

    def test_max_boundary(self):
        """최대값(45)은 유효한 번호다"""
        assert is_valid_lotto_number(45, [1, 2, 3]) is True


class TestGenerateLottoNumbers:
    """로또 번호 생성 테스트"""
    
    def test_generates_correct_count(self):
        """6개의 번호를 생성한다"""
        numbers = generate_lotto_numbers()
        assert len(numbers) == LOTTO_NUMBER_COUNT

    def test_all_numbers_in_valid_range(self):
        """모든 번호가 1~45 범위 내에 있다"""
        numbers = generate_lotto_numbers()
        assert all(LOTTO_MIN_NUMBER <= n <= LOTTO_MAX_NUMBER for n in numbers)

    def test_no_duplicate_numbers(self):
        """중복된 번호가 없다"""
        numbers = generate_lotto_numbers()
        assert len(numbers) == len(set(numbers))


class TestReadUserNumbers:
    """사용자 번호 입력 테스트"""
    
    @patch("builtins.input", side_effect=["1", "2", "3", "4", "5", "6"])
    def test_valid_input_sequence(self, mock_input):
        """올바른 6개의 번호를 순서대로 입력하면 성공한다"""
        numbers = read_user_numbers()
        assert numbers == [1, 2, 3, 4, 5, 6]

    @patch("builtins.input", side_effect=["abc", "1", "2", "3", "4", "5", "6"])
    @patch("builtins.print")
    def test_invalid_string_input(self, mock_print, mock_input):
        """문자열 입력 시 에러 메시지를 출력하고 재입력을 요청한다"""
        numbers = read_user_numbers()
        assert len(numbers) == LOTTO_NUMBER_COUNT
        mock_print.assert_any_call("숫자를 입력해 주세요.")

    @patch("builtins.input", side_effect=["1", "1", "2", "3", "4", "5", "6"])
    @patch("builtins.print")
    def test_duplicate_input(self, mock_print, mock_input):
        """중복된 번호 입력 시 재입력을 요청하여 중복 없는 6개를 받는다"""
        numbers = read_user_numbers()
        assert len(numbers) == LOTTO_NUMBER_COUNT
        assert len(set(numbers)) == LOTTO_NUMBER_COUNT

    @patch("builtins.input", side_effect=["50", "1", "2", "3", "4", "5", "6"])
    @patch("builtins.print")
    def test_out_of_range_input(self, mock_print, mock_input):
        """범위를 벗어난 번호 입력 시 재입력을 요청하여 유효한 범위의 번호를 받는다"""
        numbers = read_user_numbers()
        assert all(LOTTO_MIN_NUMBER <= n <= LOTTO_MAX_NUMBER for n in numbers)


class TestCountMatch:
    """번호 일치 개수 계산 테스트"""
    
    def test_no_matches(self):
        """일치하는 번호가 없으면 0을 반환한다"""
        assert count_match([1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]) == 0

    def test_all_matches(self):
        """모든 번호가 일치하면 6을 반환한다"""
        assert count_match([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]) == 6

    def test_partial_matches(self):
        """일부 번호만 일치하면 일치하는 개수를 반환한다"""
        assert count_match([1, 2, 3, 4, 5, 6], [1, 2, 3, 7, 8, 9]) == 3

    def test_different_order_matches(self):
        """순서가 다르더라도 일치하는 번호를 정확히 계산한다"""
        assert count_match([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]) == 6


class TestPrintResult:
    """결과 출력 및 등수 판정 테스트"""
    
    @patch("builtins.print")
    def test_first_prize(self, mock_print):
        """6개 일치 시 1등을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 6)
        mock_print.assert_any_call("1st")

    @patch("builtins.print")
    def test_second_prize(self, mock_print):
        """5개 일치 시 2등을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 7], 5)
        mock_print.assert_any_call("2nd")

    @patch("builtins.print")
    def test_third_prize(self, mock_print):
        """4개 일치 시 3등을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 7, 8], 4)
        mock_print.assert_any_call("3rd")

    @patch("builtins.print")
    def test_fourth_prize(self, mock_print):
        """3개 일치 시 4등을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 7, 8, 9], 3)
        mock_print.assert_any_call("4th")

    @patch("builtins.print")
    def test_no_prize(self, mock_print):
        """3개 미만 일치 시 낙첨을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], 0)
        mock_print.assert_any_call("fail")