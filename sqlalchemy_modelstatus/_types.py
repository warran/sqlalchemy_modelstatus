# -*- encoding: utf-8 -*-

import enum


class EnumEqString(str):
    def __eq__(self, other):
        if isinstance(other, str):
            return super(EnumEqString, self).__eq__(other)
        elif isinstance(other, enum.Enum):
            return super(EnumEqString, self).__eq__(other.value)
        else:
            return NotImplemented


class StrinqEqEnum(enum.Enum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return NotImplemented
