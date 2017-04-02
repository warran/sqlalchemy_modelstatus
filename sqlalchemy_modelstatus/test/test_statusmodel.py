# -*- encoding: utf-8 -*-

import pytest
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_modelstatus.statusmodel import *


@pytest.fixture
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


@pytest.fixture
def status_dict_action_based():
    return {
        'actions': {
            'grant_access': [('access_pending', 'tc_pending'),
                             ('access_denied', ['offline', 'locked', 'tc_pending'], PREVIOUS_STATUS)],
            'deny_access': ('tc_pending', 'access_denied'),
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


@pytest.fixture(scope="module")
def model_with_status(db_engine, status_dict_status_based):
    class SimpleModelWithStatus(StatusModel, Base):
        __table__ = 'simple_model_status'
        __status__ = status_dict_status_based

    db_engine.create_all()

    yield SimpleModelWithStatus

    db_engine.drop_all()


@pytest.fixture(scope="module")
def model_with_action_status(db_engine, status_dict_action_based):
    class SimpleModelWithStatus:
        __table__ = 'action_model_status'
        __status__ = status_dict_action_based

    db_engine.create_all()

    yield SimpleModelWithStatus

    db_engine.drop_all()


def test_has_status_attr(model_with_status, model_with_action_status):
    pass


def test_has_checks(model_with_status, model_with_action_status):
    pass


def test_has_group_checks(model_with_status, model_with_action_status):
    pass


def test_simple_transitions(model_with_status, model_with_action_status):
    pass


def test_previous_transition(model_with_status, model_with_action_status):
    pass


def test_any_transition(model_with_status, model_with_action_status):
    pass
