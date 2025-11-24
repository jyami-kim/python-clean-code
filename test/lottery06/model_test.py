"""
lottery06 도메인 모델 테스트
Pydantic 검증 로직을 테스트합니다.
"""

import pytest
from pydantic import ValidationError

from src.lottery06.model import LottoNumbers, LottoResult


class TestLottoNumbers:
    """LottoNumbers 도메인 모델 테스트"""

    def test_valid_lotto_numbers(self):
        """유효한 로또 번호 6개로 모델 생성 성공"""
        numbers = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        assert numbers.numbers == [1, 10, 20, 30, 40, 45]

    def test_numbers_count_must_be_6(self):
        """로또 번호는 정확히 6개여야 함"""
        # 5개만 입력
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[1, 10, 20, 30, 40])

        errors = exc_info.value.errors()
        assert any("at least 6 items" in str(err["msg"]).lower() for err in errors)

        # 7개 입력
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[1, 10, 20, 30, 40, 45, 44])

        errors = exc_info.value.errors()
        assert any("at most 6 items" in str(err["msg"]).lower() for err in errors)

    def test_numbers_must_be_in_range_1_to_45(self):
        """로또 번호는 1~45 범위여야 함"""
        # 0 포함 (범위 미만)
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[0, 10, 20, 30, 40, 45])

        errors = exc_info.value.errors()
        assert any("greater than or equal" in str(err["msg"]).lower() for err in errors)

        # 46 포함 (범위 초과)
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[1, 10, 20, 30, 40, 46])

        errors = exc_info.value.errors()
        assert any("less than or equal" in str(err["msg"]).lower() for err in errors)

        # 음수
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[-1, 10, 20, 30, 40, 45])

        errors = exc_info.value.errors()
        assert any("greater than or equal" in str(err["msg"]).lower() for err in errors)

    def test_numbers_must_be_unique(self):
        """로또 번호는 중복될 수 없음"""
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[1, 10, 10, 30, 40, 45])

        errors = exc_info.value.errors()
        assert any("중복" in str(err["msg"]) for err in errors)

    def test_numbers_coerce_to_integers(self):
        """Pydantic은 변환 가능한 타입을 자동으로 정수로 변환함"""
        # 소수는 정수로 변환됨 (1.5 -> 1)
        numbers = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        assert all(isinstance(n, int) for n in numbers.numbers)

        # 문자열 숫자도 정수로 변환됨
        numbers = LottoNumbers(numbers=["1", "10", "20", "30", "40", "45"])
        assert numbers.numbers == [1, 10, 20, 30, 40, 45]
        assert all(isinstance(n, int) for n in numbers.numbers)

        # 변환 불가능한 문자열은 에러
        with pytest.raises(ValidationError):
            LottoNumbers(numbers=["abc", "10", "20", "30", "40", "45"])

    def test_edge_cases_min_and_max(self):
        """경계값 테스트 (1과 45)"""
        # 최소값들
        numbers = LottoNumbers(numbers=[1, 2, 3, 4, 5, 6])
        assert numbers.numbers == [1, 2, 3, 4, 5, 6]

        # 최대값들
        numbers = LottoNumbers(numbers=[40, 41, 42, 43, 44, 45])
        assert numbers.numbers == [40, 41, 42, 43, 44, 45]

        # 최소/최대 혼합
        numbers = LottoNumbers(numbers=[1, 2, 43, 44, 45, 22])
        assert numbers.numbers == [1, 2, 43, 44, 45, 22]


class TestLottoResult:
    """LottoResult 도메인 모델 테스트"""

    def test_valid_lotto_result(self):
        """유효한 로또 결과 모델 생성 성공"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 25, 35, 44])

        result = LottoResult(lotto_numbers=lotto, user_numbers=user, match_count=3, rank="4th")

        assert result.lotto_numbers.numbers == [1, 10, 20, 30, 40, 45]
        assert result.user_numbers.numbers == [1, 10, 20, 25, 35, 44]
        assert result.match_count == 3
        assert result.rank == "4th"

    def test_result_with_all_match(self):
        """6개 모두 일치 (1등) 결과"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])

        result = LottoResult(lotto_numbers=lotto, user_numbers=user, match_count=6, rank="1st")

        assert result.match_count == 6
        assert result.rank == "1st"

    def test_result_with_no_match(self):
        """일치하는 번호 없음 (낙첨)"""
        lotto = LottoNumbers(numbers=[1, 2, 3, 4, 5, 6])
        user = LottoNumbers(numbers=[40, 41, 42, 43, 44, 45])

        result = LottoResult(lotto_numbers=lotto, user_numbers=user, match_count=0, rank="fail")

        assert result.match_count == 0
        assert result.rank == "fail"

    def test_result_requires_valid_lotto_numbers(self):
        """LottoResult는 유효한 LottoNumbers를 요구함"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])

        # 잘못된 user_numbers 전달 시 ValidationError
        with pytest.raises(ValidationError):
            LottoResult(
                lotto_numbers=lotto,
                user_numbers=[1, 10, 20, 30, 40, 45],  # LottoNumbers가 아님
                match_count=6,
                rank="1st",
            )

    def test_result_match_count_is_integer(self):
        """match_count는 정수여야 함"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 25, 35, 44])

        # 실수 전달
        with pytest.raises(ValidationError):
            LottoResult(lotto_numbers=lotto, user_numbers=user, match_count=3.5, rank="4th")

    def test_result_rank_is_string(self):
        """rank는 문자열이어야 함"""
        lotto = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        user = LottoNumbers(numbers=[1, 10, 20, 25, 35, 44])

        result = LottoResult(lotto_numbers=lotto, user_numbers=user, match_count=3, rank="4th")

        assert isinstance(result.rank, str)
        assert result.rank == "4th"


class TestLottoNumbersIntegration:
    """LottoNumbers 통합 시나리오 테스트"""

    def test_multiple_validation_errors(self):
        """여러 검증 오류가 동시에 발생하는 경우"""
        # 개수 부족 + 중복 + 범위 초과
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[1, 1, 50])  # 3개만, 중복, 50은 범위 초과

        errors = exc_info.value.errors()
        # 최소 1개 이상의 에러 발생
        assert len(errors) >= 1

    def test_empty_list(self):
        """빈 리스트는 허용되지 않음"""
        with pytest.raises(ValidationError) as exc_info:
            LottoNumbers(numbers=[])

        errors = exc_info.value.errors()
        assert any("at least 6 items" in str(err["msg"]).lower() for err in errors)

    def test_none_value(self):
        """None 값은 허용되지 않음"""
        with pytest.raises(ValidationError):
            LottoNumbers(numbers=None)

    def test_model_serialization(self):
        """모델을 dict로 직렬화 가능"""
        numbers = LottoNumbers(numbers=[1, 10, 20, 30, 40, 45])
        data = numbers.model_dump()

        assert data == {"numbers": [1, 10, 20, 30, 40, 45]}

    def test_model_json_schema(self):
        """JSON 스키마 생성 가능 (문서화 용도)"""
        schema = LottoNumbers.model_json_schema()

        assert "properties" in schema
        assert "numbers" in schema["properties"]
        assert schema["properties"]["numbers"]["minItems"] == 6
        assert schema["properties"]["numbers"]["maxItems"] == 6
