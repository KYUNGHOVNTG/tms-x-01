"""
Auth Domain

레거시 TMS 시스템 연동을 위한 인증 도메인입니다.
Oracle DB를 사용한 비동기 로그인을 처리합니다.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.core.database import get_oracle_db
from server.app.core.logging import get_logger
from server.app.domain.auth.schemas import LoginRequest, LoginResponse
from server.app.domain.auth.service import AuthService

logger = get_logger(__name__)

# ====================
# Router
# ====================

router = APIRouter(
    prefix="/auth",
    tags=["Auth (Legacy TMS)"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="레거시 TMS 로그인",
    description="""
    레거시 TMS Oracle DB를 사용하여 사용자 로그인을 처리합니다.

    - **username**: 사용자 ID
    - **password**: 비밀번호

    성공 시 사용자 정보와 임시 토큰을 반환합니다.
    (추후 JWT 토큰으로 대체 예정)
    """,
    responses={
        200: {
            "description": "로그인 성공",
            "content": {
                "application/json": {
                    "example": {
                        "user_id": "user001",
                        "user_name": "홍길동",
                        "token": "temp_token_abc123",
                        "message": "로그인 성공"
                    }
                }
            }
        },
        400: {
            "description": "요청 데이터 검증 실패",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "사용자 ID는 빈 문자열일 수 없습니다"
                    }
                }
            }
        },
        401: {
            "description": "인증 실패 (사용자 없음 또는 비밀번호 불일치)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "사용자 ID 또는 비밀번호가 올바르지 않습니다"
                    }
                }
            }
        },
        500: {
            "description": "서버 오류",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "로그인 처리 중 오류가 발생했습니다"
                    }
                }
            }
        }
    }
)
async def login(
    request: LoginRequest,
    oracle_db: AsyncSession = Depends(get_oracle_db)
) -> LoginResponse:
    """
    레거시 TMS 로그인

    Oracle DB를 사용하여 사용자 인증을 처리합니다.
    """
    # 서비스 인스턴스 생성
    service = AuthService(oracle_db)

    # 서비스 실행
    result = await service.execute(request)

    # 결과 처리
    if not result.success:
        # 에러 타입에 따라 적절한 HTTP 상태 코드 반환
        error_message = result.error or "로그인 처리 중 오류가 발생했습니다"

        # ValidationException 또는 NotFoundException이면 401 반환
        if "찾을 수 없습니다" in error_message or "일치하지 않습니다" in error_message or "올바르지 않습니다" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_message
            )
        elif "빈 문자열" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_message
            )

    # 성공 시 데이터 반환
    return result.data


__all__ = [
    "router",
    "LoginRequest",
    "LoginResponse",
    "AuthService",
]
