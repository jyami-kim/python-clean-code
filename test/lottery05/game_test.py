"""
lottery05/game.py 테스트
IO 의존성을 제거한 버전의 테스트
"""

from unittest.mock import Mock

from src.lottery05 import (
    LOTTO_MAX_NUMBER,
    LOTTO_MIN_NUMBER,
    LOTTO_NUMBER_COUNT,
    count_match,
    generate_lotto_numbers,
    get_rank,
    is_valid_lotto_number,
    print_result,
    read_user_numbers,
)


class Test:
    def test_fail(self):
        vaule = False
        assert vaule is True


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
    """사용자 번호 입력 테스트 - IO 의존성 주입 방식"""

    def test_valid_input_sequence(self):
        """올바른 6개의 번호를 순서대로 입력하면 성공한다"""
        # Mock 함수 생성
        mock_input = Mock(side_effect=["1", "2", "3", "4", "5", "6"])
        mock_print = Mock()

        # IO 의존성 주입
        numbers = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert numbers == [1, 2, 3, 4, 5, 6]
        assert mock_input.call_count == 6
        assert mock_print.call_count == 0  # 에러 없으므로 print 안 됨

    def test_invalid_string_input(self):
        """문자열 입력 시 에러 메시지를 출력하고 재입력을 요청한다"""
        mock_input = Mock(side_effect=["abc", "1", "2", "3", "4", "5", "6"])
        mock_print = Mock()

        numbers = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert len(numbers) == LOTTO_NUMBER_COUNT
        # "숫자를 입력해 주세요." 메시지가 출력되었는지 확인
        mock_print.assert_any_call("숫자를 입력해 주세요.")

    def test_duplicate_input(self):
        """중복된 번호 입력 시 재입력을 요청하여 중복 없는 6개를 받는다"""
        mock_input = Mock(side_effect=["1", "1", "2", "3", "4", "5", "6"])
        mock_print = Mock()

        numbers = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert len(numbers) == LOTTO_NUMBER_COUNT
        assert len(set(numbers)) == LOTTO_NUMBER_COUNT
        # 중복 에러 메시지가 출력되었는지 확인
        assert mock_print.call_count > 0

    def test_out_of_range_input(self):
        """범위를 벗어난 번호 입력 시 재입력을 요청하여 유효한 범위의 번호를 받는다"""
        mock_input = Mock(side_effect=["50", "1", "2", "3", "4", "5", "6"])
        mock_print = Mock()

        numbers = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert all(LOTTO_MIN_NUMBER <= n <= LOTTO_MAX_NUMBER for n in numbers)
        # 범위 에러 메시지가 출력되었는지 확인
        assert any(f"{LOTTO_MIN_NUMBER}~{LOTTO_MAX_NUMBER}" in str(call) for call in mock_print.call_args_list)

    def test_multiple_errors_in_sequence(self):
        """여러 종류의 에러가 섞여있어도 올바르게 처리한다"""
        mock_input = Mock(
            side_effect=[
                "abc",  # 문자열 에러
                "0",  # 범위 에러
                "1",  # 정상
                "1",  # 중복 에러
                "2",  # 정상
                "3",
                "4",
                "5",
                "6",
            ]
        )
        mock_print = Mock()

        numbers = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert len(numbers) == LOTTO_NUMBER_COUNT
        assert numbers == [1, 2, 3, 4, 5, 6]
        # 에러 메시지가 여러 번 출력되었는지 확인
        assert mock_print.call_count == 3  # 3번의 에러


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


class TestGetRank:
    """등수 판정 테스트 - IO에서 분리된 순수 함수"""

    def test_first_prize(self):
        """6개 일치 시 1등을 반환한다"""
        assert get_rank(6) == "1st"

    def test_second_prize(self):
        """5개 일치 시 2등을 반환한다"""
        assert get_rank(5) == "2nd"

    def test_third_prize(self):
        """4개 일치 시 3등을 반환한다"""
        assert get_rank(4) == "3rd"

    def test_fourth_prize(self):
        """3개 일치 시 4등을 반환한다"""
        assert get_rank(3) == "4th"

    def test_no_prize_zero(self):
        """0개 일치 시 낙첨을 반환한다"""
        assert get_rank(0) == "fail"

    def test_no_prize_one(self):
        """1개 일치 시 낙첨을 반환한다"""
        assert get_rank(1) == "fail"

    def test_no_prize_two(self):
        """2개 일치 시 낙첨을 반환한다"""
        assert get_rank(2) == "fail"


class TestPrintResult:
    """결과 출력 테스트"""

    def test_prints_lottery_and_user_numbers(self, capsys):
        """당첨 번호와 사용자 번호를 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 6)

        captured = capsys.readouterr()
        assert "result:" in captured.out
        assert "[1, 2, 3, 4, 5, 6]" in captured.out
        assert "mine:" in captured.out

    def test_prints_first_prize(self, capsys):
        """6개 일치 시 1등을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 6)

        captured = capsys.readouterr()
        assert "1st" in captured.out

    def test_prints_second_prize(self, capsys):
        """5개 일치 시 2등을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 7], 5)

        captured = capsys.readouterr()
        assert "2nd" in captured.out

    def test_prints_fail(self, capsys):
        """3개 미만 일치 시 낙첨을 출력한다"""
        print_result([1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], 0)

        captured = capsys.readouterr()
        assert "fail" in captured.out
