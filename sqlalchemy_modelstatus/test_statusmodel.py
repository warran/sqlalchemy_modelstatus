# -*- encoding: utf-8 -*-

import pytest

from .statusmodel import *


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

@pytest.fixture
def SimpleModelWithStatus():
    pass
