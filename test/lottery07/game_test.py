"""
lottery07 게임 로직 테스트
Generator 주입을 사용한 게임 로직 테스트
"""

from unittest.mock import Mock

from src.lottery07.game import count_match, get_rank, play_game, read_user_numbers
from src.lottery07.generator import AutoLottoGenerator, FixedLottoGenerator
from src.lottery07.model import LottoNumbers


class TestReadUserNumbers:
    """사용자 입력 함수 테스트"""

    def test_read_valid_input(self):
        """유효한 입력 처리"""
        mock_input = Mock(return_value="1, 10, 20, 30, 40, 45")
        mock_print = Mock()

        result = read_user_numbers(input_func=mock_input, print_func=mock_print)

        assert isinstance(result, LottoNumbers)
        assert result.numbers == [1, 10, 20, 30, 40, 45]


class TestCountMatch:
    """일치 개수 계산 함수 테스트"""

    def test_count_all_match(self):
        """6개 모두 일치"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])

        assert count_match(lotto, user) == 6

    def test_count_partial_match(self):
        """일부만 일치"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 25, 35, 44])

        assert count_match(lotto, user) == 3


class TestGetRank:
    """등수 계산 함수 테스트"""

    def test_rank_calculations(self):
        """등수 계산"""
        assert get_rank(6) == "1st"
        assert get_rank(5) == "2nd"
        assert get_rank(4) == "3rd"
        assert get_rank(3) == "4th"
        assert get_rank(2) == "fail"


class TestPlayGameWithGenerator:
    """Generator 주입을 사용한 게임 테스트"""

    def test_play_game_with_fixed_generator(self):
        """고정 Generator로 게임 실행"""
        # 고정 로또 번호: [1, 10, 20, 30, 40, 45]
        lotto_generator = FixedLottoGenerator([1, 10, 20, 30, 40, 45])

        # 사용자 입력: [1, 10, 20, 25, 35, 44] (3개 일치)
        mock_input = Mock(return_value="1, 10, 20, 25, 35, 44")
        mock_print = Mock()

        result = play_game(generator=lotto_generator, input_func=mock_input, print_func=mock_print)

        assert result.lotto_numbers.numbers == [1, 10, 20, 30, 40, 45]
        assert result.user_numbers.numbers == [1, 10, 20, 25, 35, 44]
        assert result.match_count == 3
        assert result.rank == "4th"

    def test_play_game_with_auto_generator(self):
        """자동 Generator로 게임 실행"""
        auto_generator = AutoLottoGenerator()

        mock_input = Mock(return_value="1, 10, 20, 30, 40, 45")
        mock_print = Mock()

        result = play_game(generator=auto_generator, input_func=mock_input, print_func=mock_print)

        # 자동 생성이므로 번호는 예측 불가, 타입과 형식만 검증
        assert isinstance(result.lotto_numbers, LottoNumbers)
        assert result.user_numbers.numbers == [1, 10, 20, 30, 40, 45]
        assert isinstance(result.match_count, int)
        assert result.rank in ["1st", "2nd", "3rd", "4th", "fail"]

    def test_play_game_perfect_match(self):
        """1등 (6개 일치) 시나리오"""
        # 로또 번호를 미리 알고 있는 상태
        lotto_generator = FixedLottoGenerator([1, 2, 3, 4, 5, 6])

        # 사용자가 동일한 번호 입력
        mock_input = Mock(return_value="1, 2, 3, 4, 5, 6")
        mock_print = Mock()

        result = play_game(generator=lotto_generator, input_func=mock_input, print_func=mock_print)

        assert result.match_count == 6
        assert result.rank == "1st"

    def test_play_game_no_match(self):
        """낙첨 (일치 없음) 시나리오"""
        lotto_generator = FixedLottoGenerator([1, 2, 3, 4, 5, 6])

        # 전혀 다른 번호 입력
        mock_input = Mock(return_value="40, 41, 42, 43, 44, 45")
        mock_print = Mock()

        result = play_game(generator=lotto_generator, input_func=mock_input, print_func=mock_print)

        assert result.match_count == 0
        assert result.rank == "fail"

    def test_play_game_prints_result(self):
        """게임 결과 출력 확인"""
        lotto_generator = FixedLottoGenerator([1, 10, 20, 30, 40, 45])
        mock_input = Mock(return_value="1, 10, 20, 25, 35, 44")
        mock_print = Mock()

        play_game(generator=lotto_generator, input_func=mock_input, print_func=mock_print)

        # 결과 출력이 호출되었는지 확인
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("result:" in str(call) for call in calls)
        assert any("mine:" in str(call) for call in calls)
        assert any("match:" in str(call) for call in calls)
        assert any("rank:" in str(call) for call in calls)


class TestGeneratorDependencyInjection:
    """생성 전략 의존성 주입 테스트"""

    def test_different_generators_produce_different_results(self):
        """다른 Generator는 다른 결과를 생성"""
        gen1 = FixedLottoGenerator([1, 2, 3, 4, 5, 6])
        gen2 = FixedLottoGenerator([10, 20, 30, 40, 41, 42])

        mock_input = Mock(return_value="1, 2, 3, 4, 5, 6")
        mock_print = Mock()

        result1 = play_game(generator=gen1, input_func=mock_input, print_func=mock_print)
        mock_input.reset_mock()
        mock_input.return_value = "1, 2, 3, 4, 5, 6"

        result2 = play_game(generator=gen2, input_func=mock_input, print_func=mock_print)

        # 같은 사용자 입력이지만 로또 번호가 다르므로 결과도 다름
        assert result1.lotto_numbers.numbers != result2.lotto_numbers.numbers
        assert result1.match_count != result2.match_count

    def test_generator_can_be_mocked_for_testing(self):
        """테스트를 위해 Generator를 Mock으로 교체 가능"""

        class TestGenerator:
            """테스트용 Generator"""

            def generate(self) -> LottoNumbers:
                # 항상 [7, 14, 21, 28, 35, 42] 반환
                return LottoNumbers(numbers=[7, 14, 21, 28, 35, 42])

        test_generator = TestGenerator()
        mock_input = Mock(return_value="7, 14, 21, 28, 35, 42")
        mock_print = Mock()

        result = play_game(generator=test_generator, input_func=mock_input, print_func=mock_print)

        assert result.lotto_numbers.numbers == [7, 14, 21, 28, 35, 42]
        assert result.match_count == 6
        assert result.rank == "1st"
