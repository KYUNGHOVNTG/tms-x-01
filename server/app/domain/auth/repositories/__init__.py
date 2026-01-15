"""
Auth Domain Repository

레거시 TMS Oracle DB에서 사용자 정보를 조회하는 Repository입니다.
Raw SQL (text)을 사용하여 직접 쿼리를 실행합니다.
"""

from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from server.app.core.logging import get_logger
from server.app.domain.auth.schemas import UserRecord
from server.app.shared.exceptions import NotFoundException

logger = get_logger(__name__)


class AuthRepository:
    """
    인증 Repository

    레거시 TMS Oracle DB에서 사용자 정보를 조회합니다.
    ORM 매핑 없이 Native Query(text)를 사용하여 빠른 개발을 지원합니다.

    책임:
        - 사용자 조회 (username 기반)
        - Raw SQL 쿼리 실행
        - 데이터베이스 결과를 Pydantic 스키마로 변환
    """

    def __init__(self, db: AsyncSession):
        """
        Args:
            db: Oracle 데이터베이스 세션
        """
        self.db = db

    async def find_user_by_username(self, username: str) -> Optional[UserRecord]:
        """
        사용자 ID로 사용자 정보를 조회합니다.

        레거시 TMS Oracle DB에서 사용자 정보를 조회하는 Raw SQL 쿼리입니다.

        Args:
            username: 사용자 ID

        Returns:
            UserRecord: 사용자 정보 (없으면 None)

        Note:
            - 테이블명: T_USER (실제 테이블명으로 수정 필요)
            - 컬럼명: USER_ID, PASSWORD, USER_NAME (실제 컬럼명으로 수정 필요)
            - 쿼리는 placeholder를 사용하여 SQL Injection 방지
        """
        # TODO: 실제 테이블명과 컬럼명으로 수정 필요
        # 현재는 placeholder 쿼리입니다.
        # 예상 테이블: T_USER, T_MEMBER, USERS 등
        # 예상 컬럼: USER_ID, USER_NAME, PASSWORD, PWD, PASSWD 등
        query = text("""
            SELECT
                USER_ID,
                PASSWORD,
                USER_NAME
            FROM T_USER
            WHERE USER_ID = :username
        """)

        try:
            result = await self.db.execute(query, {"username": username})
            row = result.fetchone()

            if row is None:
                logger.info(
                    f"User not found in Oracle DB",
                    extra={"username": username}
                )
                return None

            # Row를 Pydantic 모델로 변환
            # row는 tuple 형태이므로 컬럼 순서에 맞춰 매핑
            user_record = UserRecord(
                user_id=row[0],      # USER_ID
                password=row[1],     # PASSWORD
                user_name=row[2],    # USER_NAME
            )

            logger.info(
                f"User found in Oracle DB",
                extra={
                    "username": username,
                    "user_name": user_record.user_name
                }
            )

            return user_record

        except Exception as e:
            logger.error(
                f"Error querying Oracle DB for user",
                exc_info=True,
                extra={"username": username, "error": str(e)}
            )
            raise

    async def verify_user_exists(self, username: str) -> bool:
        """
        사용자 존재 여부를 확인합니다.

        Args:
            username: 사용자 ID

        Returns:
            bool: 사용자 존재 여부
        """
        user = await self.find_user_by_username(username)
        return user is not None
