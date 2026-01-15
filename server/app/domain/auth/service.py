"""
Auth Domain Service

레거시 TMS Oracle DB를 통한 사용자 로그인을 처리하는 서비스입니다.
"""

import secrets
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from server.app.core.logging import get_logger
from server.app.shared.base import BaseService
from server.app.shared.types import ServiceResult
from server.app.shared.exceptions import ValidationException, NotFoundException
from server.app.domain.auth.schemas import LoginRequest, LoginResponse
from server.app.domain.auth.repositories import AuthRepository

logger = get_logger(__name__)


class AuthService(BaseService[LoginRequest, LoginResponse]):
    """
    인증 서비스

    레거시 TMS Oracle DB를 사용한 사용자 로그인을 처리합니다.

    책임:
        - 사용자 로그인 검증
        - 비밀번호 확인
        - 임시 토큰 생성 (추후 JWT로 대체 예정)

    흐름:
        1. 요청 검증
        2. 사용자 조회 (Repository)
        3. 비밀번호 검증 (현재는 더미)
        4. 토큰 생성
        5. 응답 반환
    """

    def __init__(self, db: AsyncSession):
        """
        Args:
            db: Oracle 데이터베이스 세션
        """
        super().__init__(db)
        self.repository = AuthRepository(db)

    async def execute(
        self,
        request: LoginRequest,
        user_id: Optional[int] = None,
        **kwargs
    ) -> ServiceResult[LoginResponse]:
        """
        로그인 요청을 실행합니다.

        Args:
            request: 로그인 요청 (username, password)
            user_id: 요청한 사용자 ID (선택, 로그인에서는 사용하지 않음)
            **kwargs: 추가 컨텍스트

        Returns:
            ServiceResult[LoginResponse]: 로그인 결과

        Raises:
            ValidationException: 입력 검증 실패
            NotFoundException: 사용자를 찾을 수 없음
        """
        try:
            # 실행 전 훅
            await self.before_execute(request)

            # 1. 요청 검증
            await self.validate_request(request)

            # 2. 사용자 조회 (Repository)
            user_record = await self.repository.find_user_by_username(request.username)

            if user_record is None:
                logger.warning(
                    "Login failed: User not found",
                    extra={"username": request.username}
                )
                raise NotFoundException(
                    message=f"사용자를 찾을 수 없습니다: {request.username}"
                )

            # 3. 비밀번호 검증
            if not await self._verify_password(request.password, user_record.password):
                logger.warning(
                    "Login failed: Invalid password",
                    extra={"username": request.username}
                )
                raise ValidationException(
                    message="비밀번호가 일치하지 않습니다"
                )

            # 4. 토큰 생성 (임시)
            token = self._generate_temp_token()

            # 5. 응답 생성
            response = LoginResponse(
                user_id=user_record.user_id,
                user_name=user_record.user_name,
                token=token,
                message="로그인 성공"
            )

            # 6. 성공 결과
            result = ServiceResult.ok(
                response,
                metadata={
                    "username": request.username,
                    "user_id": user_record.user_id,
                }
            )

            logger.info(
                "Login successful",
                extra={
                    "username": request.username,
                    "user_id": user_record.user_id,
                }
            )

            # 실행 후 훅
            await self.after_execute(request, result)

            return result

        except (ValidationException, NotFoundException) as e:
            # 예상된 예외는 그대로 전달
            return await self.handle_error(e, request)
        except Exception as e:
            # 예상치 못한 예외 처리
            logger.error(
                "Unexpected error during login",
                exc_info=True,
                extra={"username": request.username}
            )
            return await self.handle_error(e, request)

    async def validate_request(self, request: LoginRequest) -> None:
        """
        로그인 요청 데이터의 유효성을 검증합니다.

        Args:
            request: 검증할 요청

        Raises:
            ValidationException: 유효성 검증 실패 시
        """
        # Pydantic이 기본 검증(길이 등)을 수행
        # 추가 비즈니스 규칙 검증
        if not request.username.strip():
            raise ValidationException("사용자 ID는 빈 문자열일 수 없습니다")

        if not request.password.strip():
            raise ValidationException("비밀번호는 빈 문자열일 수 없습니다")

    async def _verify_password(self, input_password: str, stored_password: str) -> bool:
        """
        비밀번호를 검증합니다.

        현재는 더미 구현입니다. 레거시 시스템의 암호화 방식을 확인한 후
        실제 암호화 검증 로직으로 대체해야 합니다.

        TODO: 레거시 시스템의 암호화 방식 확인 후 구현
            - MD5, SHA-1, SHA-256 등의 해시 알고리즘
            - bcrypt, PBKDF2 등의 key derivation 함수
            - 평문 저장 (보안상 권장하지 않음)

        Args:
            input_password: 사용자가 입력한 비밀번호
            stored_password: DB에 저장된 비밀번호

        Returns:
            bool: 비밀번호 일치 여부
        """
        # 임시 구현: 평문 비교 (나중에 수정 필요)
        # 실제로는 레거시 시스템의 암호화 방식에 맞춰 검증해야 함
        return input_password == stored_password

    def _generate_temp_token(self) -> str:
        """
        임시 토큰을 생성합니다.

        현재는 단순한 랜덤 문자열을 생성합니다.
        추후 JWT 기반 토큰으로 대체할 예정입니다.

        TODO: JWT 토큰 생성 구현
            - python-jose 라이브러리 사용
            - 토큰에 user_id, exp 등의 클레임 포함
            - 액세스 토큰 + 리프레시 토큰 구조

        Returns:
            str: 임시 인증 토큰
        """
        # 임시 구현: 안전한 랜덤 문자열
        return f"temp_token_{secrets.token_urlsafe(32)}"

    async def handle_error(
        self,
        error: Exception,
        request: LoginRequest
    ) -> ServiceResult[LoginResponse]:
        """
        에러를 처리하고 적절한 결과를 반환합니다.

        Args:
            error: 발생한 예외
            request: 요청 데이터

        Returns:
            ServiceResult: 에러 결과
        """
        # 에러 로깅 (비밀번호는 로그에서 제외)
        logger.error(
            f"Error in AuthService: {str(error)}",
            exc_info=isinstance(error, Exception) and not isinstance(error, (ValidationException, NotFoundException)),
            extra={"username": request.username}
        )

        # 에러 타입에 따라 다른 메시지 반환
        if isinstance(error, ValidationException):
            error_message = str(error)
        elif isinstance(error, NotFoundException):
            error_message = "사용자 ID 또는 비밀번호가 올바르지 않습니다"  # 보안상 모호하게 표현
        else:
            error_message = "로그인 처리 중 오류가 발생했습니다"

        return ServiceResult.fail(
            error_message,
            metadata={
                "error_type": type(error).__name__,
                "username": request.username,
            }
        )
