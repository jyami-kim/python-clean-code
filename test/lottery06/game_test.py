"""
lottery06 게임 로직 테스트
도메인 모델과 게임 로직을 함께 테스트합니다.
"""

from unittest.mock import Mock

from src.lottery06.game import (
    count_match,
    generate_lotto_numbers,
    get_rank,
    play_game,
    read_user_numbers,
)
from src.lottery06.model import LottoNumbers


class TestGenerateLottoNumbers:
    """로또 번호 생성 함수 테스트"""

    def test_generate_returns_lotto_numbers_model(self):
        """생성된 번호는 LottoNumbers 모델이어야 함"""
        result = generate_lotto_numbers()
        assert isinstance(result, LottoNumbers)

    def test_generate_returns_6_unique_numbers(self):
        """생성된 번호는 6개의 중복 없는 숫자"""
        result = generate_lotto_numbers()
        assert len(result.numbers) == 6
        assert len(set(result.numbers)) == 6  # 중복 없음

    def test_generate_numbers_in_valid_range(self):
        """생성된 번호는 1~45 범위"""
        result = generate_lotto_numbers()
        assert all(1 <= num <= 45 for num in result.numbers)

    def test_generate_multiple_times(self):
        """여러 번 생성해도 항상 유효한 모델 반환"""
        for _ in range(10):
            result = generate_lotto_numbers()
            assert isinstance(result, LottoNumbers)
            assert len(result.numbers) == 6


class TestReadUserNumbers:
    """사용자 입력 함수 테스트 (의존성 주입)"""

    def test_read_valid_input(self):
        """유효한 입력 처리"""
        mock_input = Mock(return_value="1, 10, 20, 30, 40, 45")
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert isinstance(result, LottoNumbers)
        assert result.numbers == [1, 10, 20, 30, 40, 45]
        mock_input.assert_called_once()

    def test_read_input_with_spaces(self):
        """공백이 있는 입력도 처리 가능"""
        mock_input = Mock(return_value="1,  10,  20,  30,  40,  45")
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert result.numbers == [1, 10, 20, 30, 40, 45]

    def test_read_input_retry_on_non_numeric(self):
        """숫자가 아닌 입력 시 재입력 요청"""
        mock_input = Mock(side_effect=["a, b, c, d, e, f", "1, 10, 20, 30, 40, 45"])
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        assert mock_input.call_count == 2
        mock_print.assert_any_call("숫자만 입력해 주세요.")

    def test_read_input_retry_on_invalid_count(self):
        """6개가 아닌 입력 시 재입력 요청"""
        mock_input = Mock(side_effect=["1, 10, 20", "1, 10, 20, 30, 40, 45"])
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        assert mock_input.call_count == 2

    def test_read_input_retry_on_duplicate(self):
        """중복된 번호 입력 시 재입력 요청"""
        mock_input = Mock(side_effect=["1, 1, 20, 30, 40, 45", "1, 10, 20, 30, 40, 45"])
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        assert mock_input.call_count == 2

    def test_read_input_retry_on_out_of_range(self):
        """범위 밖 번호 입력 시 재입력 요청"""
        mock_input = Mock(side_effect=["0, 10, 20, 30, 40, 45", "1, 10, 20, 30, 40, 45"])
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert result.numbers == [1, 10, 20, 30, 40, 45]
        assert mock_input.call_count == 2


class TestCountMatch:
    """일치 개수 계산 함수 테스트"""

    def test_count_all_match(self):
        """6개 모두 일치"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])

        assert count_match(lotto, user) == 6

    def test_count_no_match(self):
        """일치하는 번호 없음"""
        lotto = LottoNumbers(numbers=[1, 2, 3, 4, 5, 6])
        user = LottoNumbers(numbers=[40, 41, 42, 43, 44, 45])

        assert count_match(lotto, user) == 0

    def test_count_partial_match(self):
        """일부만 일치"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 25, 35, 44])

        assert count_match(lotto, user) == 3

    def test_count_order_does_not_matter(self):
        """순서와 무관하게 일치 개수 계산"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[45, 40, 30, 20, 10, 1])

        assert count_match(lotto, user) == 6


class TestGetRank:
    """등수 계산 함수 테스트"""

    def test_rank_6_match(self):
        """6개 일치 → 1등"""
        assert get_rank(6) == "1st"

    def test_rank_5_match(self):
        """5개 일치 → 2등"""
        assert get_rank(5) == "2nd"

    def test_rank_4_match(self):
        """4개 일치 → 3등"""
        assert get_rank(4) == "3rd"

    def test_rank_3_match(self):
        """3개 일치 → 4등"""
        assert get_rank(3) == "4th"

    def test_rank_less_than_3_match(self):
        """3개 미만 일치 → 낙첨"""
        assert get_rank(2) == "fail"
        assert get_rank(1) == "fail"
        assert get_rank(0) == "fail"


class TestPlayGame:
    """게임 전체 흐름 통합 테스트"""

    def test_play_game_returns_lotto_result(self):
        """게임 실행 시 LottoResult 반환"""
        mock_input = Mock(return_value="1, 10, 20, 30, 40, 45")
        mock_print = Mock()

        result = play_game(input_func=mock_input, print_func=mock_print)

        assert result.lotto_numbers is not None
        assert result.user_numbers.numbers == [1, 10, 20, 30, 40, 45]
        assert isinstance(result.match_count, int)
        assert result.rank in ["1st", "2nd", "3rd", "4th", "fail"]

    def test_play_game_prints_result(self):
        """게임 결과 출력 확인"""
        mock_input = Mock(return_value="1, 10, 20, 30, 40, 45")
        mock_print = Mock()

        play_game(input_func=mock_input, print_func=mock_print)

        # 결과 출력이 호출되었는지 확인
        assert mock_print.call_count >= 4  # result, mine, match, rank
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("result:" in str(call) for call in calls)
        assert any("mine:" in str(call) for call in calls)
        assert any("match:" in str(call) for call in calls)
        assert any("rank:" in str(call) for call in calls)
