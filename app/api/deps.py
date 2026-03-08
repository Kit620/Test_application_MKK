"""Зависимости API: сессия БД, проверка API-ключа."""

from fastapi import Depends, Header, HTTPException

from app.config import settings
from app.db import get_db


def require_api_key(
    x_api_key: str = Header(..., alias="X-API-Key", description="Статический API ключ"),
) -> str:
    """Проверяет заголовок X-API-Key; при несовпадении возвращает 401."""
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key


ApiKey = Depends(require_api_key)
DbSession = Depends(get_db)
