# -*- encoding: utf-8 -*-

import pytest
from sqlalchemy.ext.declarative import declarative_base

from ..statusmodel import *
from ..exceptions import *


pytestmark = pytest.mark.usefixtures("db_engine")


@pytest.fixture(scope="module")
def status_dict_status_based():
    return {
        'access_pending': ('grant_access', 'tc_pending'),
        'tc_pending': [('deny_access', 'access_denied'), ('accept_tc', 'offline')],
        'access_denied': ('grant_access', ['offline', 'locked', 'tc_pending'], PREVIOUS_STATUS),
        'offline': [('deny_access', 'access_denied'), ('log_in', 'online'), ('lock', 'locked')],
        'online': ('log_out', 'offline'),
        'locked': ('reset_password', 'offline'),
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
def ModelWithStatus(db_engine, status_dict_status_based):
    class SimpleModelWithStatus(StatusModel, Base):
        __table__ = 'simple_model_status'
        __status__ = status_dict_status_based

    db_engine.create_all()

    yield SimpleModelWithStatus

    db_engine.drop_all()


@pytest.fixture(scope="module")
def ModelWithActionStatus(db_engine, status_dict_action_based):
    class SimpleModelWithStatus:
        __table__ = 'action_model_status'
        __status__ = status_dict_action_based

    db_engine.create_all()

    yield SimpleModelWithStatus

    db_engine.drop_all()


@pytest.fixture
def model_with_status(ModelWithStatus):
    mws = ModelWithStatus()
    mws.status = 'access_pending'
    return mws


@pytest.fixture
def model_with_action_status(ModelWithActionStatus):
    mwas = ModelWithActionStatus()
    mwas.status = 'access_pending'
    return mwas


def test_has_status_attr(model_with_status, model_with_action_status):
    mws = model_with_status
    mwas = model_with_action_status

    assert hasattr(mws, 'status')
    assert hasattr(mws, 'previous_status')
    assert hasattr(mwas, 'status')
    assert not hasattr(mwas, 'previous_status')


def test_has_checks(model_with_status, model_with_action_status):
    mws = model_with_status
    mwas = model_with_action_status

    # status should be access pending, it's set in the fixtures
    assert mws.is_access_pending()
    assert not mws.is_access_denied()
    assert not mws.is_tc_pending()
    assert not mws.is_ofline()
    assert not mws.is_online()
    assert not mws.is_locked()

    assert mwas.is_access_pending()
    assert not mwas.is_access_denied()
    assert not mwas.is_tc_pending()
    assert not mwas.is_ofline()
    assert not mwas.is_online()
    assert not mwas.is_locked()
    

def test_has_group_checks(model_with_status, model_with_action_status):
    mws = model_with_status
    mwas = model_with_action_status

    assert not mws.is_active()
    assert not mwas.is_active()


def test_simple_transitions(model_with_status, model_with_action_status):
    mws = model_with_status
    mwas = model_with_action_status

    assert mws.is_access_pending()
    mws.grant_access()
    assert mws.is_tc_pending()
    mws.accept_tc()
    assert mws.is_offline()
    mws.log_in()
    assert mws.is_online()
    mws.log_out()
    assert mws.is_offline()
    mws.lock()
    assert mws.is_locked()
    mws.reset_password()
    assert mws.is_offline()

    with pytest.raises(StatusTransitionException):
        mws.accept_tc()

    assert mwas.is_access_pending()
    mwas.grant_access()
    assert mwas.is_tc_pending()
    mwas.accept_tc()
    assert mwas.is_offline()
    mwas.log_in()
    assert mwas.is_online()
    mwas.log_out()
    assert mwas.is_offline()
    mwas.lock()
    assert mwas.is_locked()
    mwas.reset_password()
    assert mwas.is_offline()

    with pytest.raises(StatusTransitionException):
        mwas.accept_tc()


def test_previous_transition(model_with_status):
    mws = model_with_status

    mws.grant_access()
    mws.deny_access()
    mws.grant_access()

    assert mws.is_tc_pending()

    mws.accept_tc()
    mws.deny_access()
    mws.grant_access()

    assert mws.is_offline()


def test_any_transition(model_with_action_status):
    mwas = model_with_action_status

    mwas.grant_access()
    assert mwas.is_tc_pending()
    mwas.deny_access()
    assert mwas.is_access_denied()
    mwas.grant_access()
    assert mwas.is_offline()
    mwas.deny_access()
    assert mwas.is_access_denied()
