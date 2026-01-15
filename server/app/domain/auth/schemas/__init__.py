"""
Auth Domain Schemas

로그인 요청/응답 및 인증 관련 Pydantic 스키마를 정의합니다.
"""

from pydantic import BaseModel, Field, ConfigDict


# ====================
# Request Schemas
# ====================


class LoginRequest(BaseModel):
    """
    로그인 요청 스키마

    레거시 TMS 시스템에 로그인하기 위한 요청 데이터입니다.
    """

    username: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="사용자 ID"
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="비밀번호"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "user001",
                "password": "password123"
            }
        }
    )


# ====================
# Response Schemas
# ====================


class LoginResponse(BaseModel):
    """
    로그인 성공 응답 스키마

    로그인 성공 시 반환되는 사용자 정보 및 토큰입니다.
    """

    user_id: str = Field(..., description="사용자 ID")
    user_name: str = Field(..., description="사용자 이름")
    token: str = Field(..., description="임시 인증 토큰 (추후 JWT로 대체 예정)")
    message: str = Field(default="로그인 성공", description="응답 메시지")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user001",
                "user_name": "홍길동",
                "token": "temp_token_abc123",
                "message": "로그인 성공"
            }
        }
    )


# ====================
# Internal Schemas (Repository/Service 간 데이터 전달용)
# ====================


class UserRecord(BaseModel):
    """
    데이터베이스에서 조회된 사용자 레코드

    Repository에서 Service로 전달되는 내부 데이터 구조입니다.
    """

    user_id: str = Field(..., description="사용자 ID")
    password: str = Field(..., description="암호화된 비밀번호")
    user_name: str = Field(..., description="사용자 이름")

    model_config = ConfigDict(from_attributes=True)
