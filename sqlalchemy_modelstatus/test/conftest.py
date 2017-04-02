# -*- encoding: utf-8 -*-

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


_SQLITE_URL = "sqlite://"


@pytest.fixture(scope="session")
def db_engine():
    return create_engine(_SQLITE_URL)


@pytest.fixture(scope="session")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()

    yield session

    session.close()
