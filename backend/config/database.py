from alembic.config import Config
from alembic import command
from core.database import Base, create_engine, SQLALCHEMY_DATABASE_URL


def init():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)

    alembic_cfg = Config("/app/alembic.ini")
    command.stamp(alembic_cfg, "head")


if __name__ == '__main__':
    init()
