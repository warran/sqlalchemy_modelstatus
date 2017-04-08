# -*- encoding: utf-8 -*-

import enum


class EnumEqString(str):
    """
    Type for strings that allows them to be compared for equality
    against Enum's, just to bypass need to get out value out of them.
    """
    def __eq__(self, other):
        if isinstance(other, str):
            return super(EnumEqString, self).__eq__(other)
        elif isinstance(other, enum.Enum):
            return super(EnumEqString, self).__eq__(other.value)
        else:
            return NotImplemented


class StrinqEqEnum(enum.Enum):
    """
    Type for Enums that allows them to be compared for equality
    against strings, just to bypass need to get out value.
    """
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return NotImplemented
