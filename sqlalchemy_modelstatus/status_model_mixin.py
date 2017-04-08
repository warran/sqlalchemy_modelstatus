# -*- encoding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from .exceptions import StatusTransitionException
from ._types import EnumEqString, StrinqEqEnum
from ._utils import nested_values


_STATUS_DEF_ATTR = "__status_definition__"
_STATUS_DEF_DEFAULT = "default"
_STATUS_DEF_STATUS = "status"


def _enum_from_dict(name, dct):
    new_enum = type(name, (StrinqEqEnum,), dct)
    return new_enum


class StatusModelMixin(object):

    @declared_attr
    def statuses(cls):
        statuses = getattr(cls, _STATUS_DEF_ATTR)[_STATUS_DEF_STATUS]
        choices = set(statuses.keys()) | set(nested_values(statuses))

        enum_name = '{}Statuses'.format(cls.__name__)
        return _enum_from_dict(enum_name, {c.upper(): c for c in choices})

    @declared_attr
    def _status(cls):
        choices = cls.statuses
        default = getattr(cls, _STATUS_DEF_ATTR)[_STATUS_DEF_DEFAULT]

        return Column(types.Enum(choices), default=default)

    @hybrid_property
    def status(self):
        return EnumEqString(self._status)

    @status.setter
    def status(self, new_status):
        if new_status in self.statuses:
            new_status = new_status.value
        self._validate_transition(new_status)
        self._status = new_status

    def _validate_transition(self, new_status):
        current_status = self._status

        # we need to take into account that the field is going to be None
        # when set for the first time
        if current_status is not None:
            statuses = getattr(self, _STATUS_DEF_ATTR)[_STATUS_DEF_STATUS]
            possible_choices = statuses[current_status]

            if not new_status in possible_choices:
                raise StatusTransitionException(
                                    "Tried to perfrom illegal status change.",
                                    from_status=current_status,
                                    to_status=new_status
                )
