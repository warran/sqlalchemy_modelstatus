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
    """
    Creates Enum type using dictionary as a definition. This allows for
    dynamic Enum type creation on the fly.
    Enums created by this function can be compared for equality against
    strings without getting the value out of them.
    :param name (str): new type name
    :param dct (dict): dictionary of desired enum values.
    :return: Enum-based class
    """
    new_enum = type(name, (StrinqEqEnum,), dct)
    return new_enum


class StatusModelMixin(object):
    """
    StatusModelMixin is a SQLAlchemy Mixin that adds `status` column to
    your model. `status` column default values, as well as available choices
    can be described using `__status_definition__` class attribute.

    `__status_definition__` should be a dictionary which can have the following keys:
    * `status`: it's value should also be a dictionary. Each key in this dict will be
    treated as a valid status name. Value associated with this key can be either a
    string or a list of strings, which are valid 'next' statuses. This data is used
    for validation on setting the status.
    * `default`: value of this key should be one of the strings present in the
    `status` field. It's going to be set as the default value for the `status`.

    Additionaly this Mixin provides user with `statuses` PEP-453 compliant Enum class,
    which values can be used for setting or comparing for equality against the status.
    """

    @declared_attr
    def statuses(cls):
        """
        Attribute added to models inheriting from this mixin. It is an Enum containing
        all possible status values.
        `statuses` attribute is a PEP-435 compliant Enum class, which values can be used
        for setting or comparing for equality against the status. The Enum's possible
        values are overloaded to be able to compare and assign them directly, without
        getting out the value, so, for example
        `my_instance.status = MyClass.statuses.ACTIVE`
        is a valid expression that will set the status to ACTIVE's value. Similarly
        `my_instance.status == MyClass.statuses.ACTIVE`
        is a valid comparison that won't raise TypeError.
        :return: Enum
        """
        statuses = getattr(cls, _STATUS_DEF_ATTR)[_STATUS_DEF_STATUS]
        choices = set(statuses.keys()) | set(nested_values(statuses))

        enum_name = '{}Statuses'.format(cls.__name__)
        return _enum_from_dict(enum_name, {c.upper(): c for c in choices})

    @declared_attr
    def _status(cls):
        """
        Attribute added to models inheriting from this mixin. This attribute implements
        the actual SQLAlchemy Column with proper choices and default.
        This should not be used directly, but rather through the `status` property,
        which allows for assigning and comparison against values from `statuses` Enum, and
        has necessary safeguards that will disallow invalid status changes.
        :return: sqlalchemy.Column
        """
        choices = cls.statuses
        default = getattr(cls, _STATUS_DEF_ATTR)[_STATUS_DEF_DEFAULT]

        return Column(types.Enum(choices), default=default)

    @hybrid_property
    def status(self):
        """
        Status attribute. This attribute can be used to retrieve and set model status, as
        well as in sqlalchemy query expressions.

        :return: status value
        """
        return EnumEqString(self._status)

    @status.setter
    def status(self, new_status):
        """
        `status` attribute setter. This function takes current model status and checks
        if the transition to `new_status` is present in the `__status_definition__`. In
        case illegal transition is attempted, it throws exception.
        :param new_status: new status to be set
        :raises: StatusTransitionException
        :return: None
        """
        if new_status in self.statuses:
            new_status = new_status.value
        self._validate_transition(new_status)
        self._status = new_status

    def _validate_transition(self, new_status):
        """
        Status transition validator. Used by `status` setter.
        :param new_status: status to be set
        :raises: StatusTransitionException
        :return: None
        """
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
