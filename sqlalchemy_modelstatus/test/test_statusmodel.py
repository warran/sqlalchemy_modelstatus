# -*- encoding: utf-8 -*-

import pytest

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

from ..status_model_mixin import *
from ..exceptions import *


pytestmark = pytest.mark.usefixtures("db_engine")


@pytest.fixture(scope='module')
def status_dict_basic():
    return {
        'status': {
            'access_pending': 'tc_pending',
            'tc_pending': ['access_denied', 'offline'],
            'access_denied': ['offline', 'locked', 'tc_pending'],
            'offline': ['access_denied', 'online', 'locked'],
            'online': 'offline',
            'locked': 'offline'
        },
        'default': 'access_pending'
    }


@pytest.fixture(scope="module")
def status_dict_status_based():
    return {
        'status': {
            'access_pending': ('grant_access', 'tc_pending'),
            'tc_pending': [('deny_access', 'access_denied'), ('accept_tc', 'offline')],
            'access_denied': ('grant_access', ['offline', 'locked', 'tc_pending'], PREVIOUS_STATUS),
            'offline': [('deny_access', 'access_denied'), ('log_in', 'online'), ('lock', 'locked')],
            'online': ('log_out', 'offline'),
            'locked': ('reset_password', 'offline')
        },
        'default': 'access_pending',
        'groups': {
            'active': ['online', 'offline', 'locked']
        }
    }


@pytest.fixture(scope="module")
def status_dict_action_based():
    return {
        'actions': {
            'grant_access': [('access_pending', 'tc_pending'),
                             ('access_denied', 'offline')],
            'deny_access': (ANY_STATUS, 'access_denied'),
            'accept_tc': ('tc_pending', 'offline'),
            'log_in': ('offline', 'online'),
            'log_out': ('online', 'offline'),
            'lock': ('offline', 'locked'),
            'reset_password': ('locked', 'offline')
        },
        'groups': {
            'active': ['online', 'offline', 'locked']
        }
    }


Base = declarative_base()


# those fixtures are indirectly testing if the
# model table can be created by SQLAlchemy
@pytest.fixture(scope="module")
def ModelWithBasicStatus(db_engine, status_dict_basic):
    class ModelWithBasicStatus(StatusModelMixin, Base):
        __tablename__ = 'basic_model_status'
        __status_definition__ = status_dict_basic

        id = Column(Integer, primary_key=True)

    Base.metadata.create_all(db_engine)

    yield ModelWithBasicStatus

    Base.metadata.drop_all(db_engine)


@pytest.fixture(scope="module")
def ModelWithStatus(db_engine, status_dict_status_based):
    class SimpleModelWithStatus(StatusModelMixin, Base):
        __table__ = 'simple_model_status'
        __status_definition__ = status_dict_status_based

    Base.metadata.create_all(db_engine)

    yield SimpleModelWithStatus

    Base.metadata.drop_all(db_engine)


@pytest.fixture(scope="module")
def ModelWithActionStatus(db_engine, status_dict_action_based):
    class SimpleModelWithStatus:
        __table__ = 'action_model_status'
        __status_definition__ = status_dict_action_based

    Base.metadata.create_all(db_engine)

    yield SimpleModelWithStatus

    Base.metadata.drop_all(db_engine)


@pytest.fixture
def model_with_basic_status(ModelWithBasicStatus):
    mwbs = ModelWithBasicStatus()
    mwbs.status = 'access_pending'
    return mwbs


@pytest.fixture
def model_with_status(ModelWithStatus):
    mws = ModelWithStatus()
    return mws


@pytest.fixture
def model_with_action_status(ModelWithActionStatus):
    mwas = ModelWithActionStatus()
    return mwas


def test_has_status_attr(model_with_basic_status):
    mwbs = model_with_basic_status
    assert hasattr(mwbs, 'status')
    assert hasattr(mwbs, 'statuses')
    assert hasattr(mwbs.statuses, 'ACCESS_PENDING')


def test_get_status(model_with_basic_status):
    mwbs = model_with_basic_status
    assert mwbs.status == mwbs.statuses.ACCESS_PENDING


def test_set_status(model_with_basic_status):
    mwbs = model_with_basic_status
    mwbs.status = mwbs.statuses.TC_PENDING
    assert mwbs.status == mwbs.statuses.TC_PENDING


def test_bad_transition_exception(model_with_basic_status):
    mwbs = model_with_basic_status

    with pytest.raises(StatusTransitionException):
        mwbs.status = mwbs.statuses.LOCKED

