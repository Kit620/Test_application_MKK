"""Seed: тестовые здания, виды деятельности, организации.

Revision ID: 002
Revises: 001
Create Date: 2025-03-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text("""
            INSERT INTO buildings (id, address, latitude, longitude) VALUES
            (1, 'г. Москва, ул. Блюхера, 32/1', 55.751244, 37.618423),
            (2, 'г. Москва, ул. Ленина, 1, офис 3', 55.755826, 37.617300),
            (3, 'г. Новосибирск, ул. Красный проспект, 77', 55.030204, 82.920430)
        """)
    )
    op.execute(sa.text("SELECT setval('buildings_id_seq', (SELECT MAX(id) FROM buildings))"))

    op.execute(
        sa.text("""
            INSERT INTO activities (id, name, parent_id, level) VALUES
            (1, 'Еда', NULL, 1),
            (2, 'Мясная продукция', 1, 2),
            (3, 'Молочная продукция', 1, 2),
            (4, 'Автомобили', NULL, 1),
            (5, 'Грузовые', 4, 2),
            (6, 'Легковые', 4, 2),
            (7, 'Запчасти', 6, 3),
            (8, 'Аксессуары', 6, 3)
        """)
    )
    op.execute(sa.text("SELECT setval('activities_id_seq', (SELECT MAX(id) FROM activities))"))

    op.execute(
        sa.text("""
            INSERT INTO organizations (id, name, building_id) VALUES
            (1, 'ООО "Рога и Копыта"', 1),
            (2, 'ИП Молоков', 1),
            (3, 'ООО "Мясной двор"', 2),
            (4, 'Автозапчасти Плюс', 2),
            (5, 'СибМолоко', 3)
        """)
    )
    op.execute(sa.text("SELECT setval('organizations_id_seq', (SELECT MAX(id) FROM organizations))"))

    op.execute(
        sa.text("""
            INSERT INTO organization_phones (id, organization_id, phone_number) VALUES
            (1, 1, '2-222-222'),
            (2, 1, '3-333-333'),
            (3, 1, '8-923-666-13-13'),
            (4, 2, '8-383-123-45-67'),
            (5, 3, '8-495-111-22-33'),
            (6, 4, '8-495-444-55-66'),
            (7, 5, '8-383-777-88-99')
        """)
    )
    op.execute(sa.text("SELECT setval('organization_phones_id_seq', (SELECT MAX(id) FROM organization_phones))"))

    op.execute(
        sa.text("""
            INSERT INTO organization_activities (organization_id, activity_id) VALUES
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 2),
            (4, 7),
            (4, 8),
            (5, 3)
        """)
    )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM organization_activities"))
    op.execute(sa.text("DELETE FROM organization_phones"))
    op.execute(sa.text("DELETE FROM organizations"))
    op.execute(sa.text("DELETE FROM activities"))
    op.execute(sa.text("DELETE FROM buildings"))
