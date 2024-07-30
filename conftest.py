from sqlalchemy import create_engine
import pytest

from sqlalchemy.orm import clear_mappers, sessionmaker

from orm import metadata, start_mappers

@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(in_memory_db)()
    clear_mappers()
