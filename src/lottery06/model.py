from typing import List

from pydantic import BaseModel, Field, conint, field_validator

from src.lottery06.const import LOTTO_MAX_NUMBER, LOTTO_MIN_NUMBER, LOTTO_NUMBER_COUNT

# 개별 로또 번호 타입 (1~45)
LottoNumber = conint(ge=LOTTO_MIN_NUMBER, le=LOTTO_MAX_NUMBER)


class LottoNumbers(BaseModel):
    """로또 번호 6개 묶음 도메인 모델"""

    numbers: List[LottoNumber] = Field(
        ...,
        min_length=LOTTO_NUMBER_COUNT,
        max_length=LOTTO_NUMBER_COUNT,
        description="로또 번호 6개",
    )

    @field_validator("numbers")
    @classmethod
    def validate_unique(cls, v: List[int]) -> List[int]:
        """번호 중복 여부 검사"""
        if len(set(v)) != len(v):
            raise ValueError("번호는 서로 중복될 수 없습니다.")
        return v


class LottoResult(BaseModel):
    """게임 결과 도메인 모델"""

    lotto_numbers: LottoNumbers
    user_numbers: LottoNumbers
    match_count: int
    rank: str
