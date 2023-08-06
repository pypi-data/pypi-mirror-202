from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from fastapi_myhelper.sqlalchemy.utils import get_non_unique_fields as src_get_non_unique_fields


async def get_non_unique_fields(
        model: SQLModel,
        data: SQLModel,
        session: AsyncSession,
) -> list[str]:
    return await src_get_non_unique_fields(
        model=model,
        data=data,
        session=session
    )