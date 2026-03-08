# REST API: Справочник организаций, зданий и деятельностей

REST API по тестовому заданию. Стек: FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL.

## Развёртывание

```bash
docker-compose up -d --build
```

API доступен на порту **8888**. Проверка: http://localhost:8888/health  
Документация и вызов методов: http://localhost:8888/docs (Swagger UI).  
Для запросов к API нужен заголовок `X-API-Key`. Ключ в compose: `test-organizations-api-key`.
