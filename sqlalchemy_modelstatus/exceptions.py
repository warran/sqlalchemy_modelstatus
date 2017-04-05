# -*- encoding: utf-8 -*-

class StatusTransitionException(Exception):
    """
    Exception that gets thrown whenever wrong status transition is
    attempted.
    You can give two optional argumments to the initializer: from_status
    and to_status, which can additionally describe the attempt.
    """

    def __init__(self, message, from_status=None, to_status=None):
        super(StatusTransitionException, self).__init__(message)
        self.from_status = from_status
        self.to_status = to_status

    def __repr__(self):
        inv_trans_str = "\nTransition from {} to {} is invalid." \
                        if self.from_status and self.to_status \
                        else ""
        return "{}{}".format(self.message, inv_trans_str)


class BadStatusDefinitionException(Exception):
    """
    Exception to be thrown when the __status__ definition is not
    written according to the requirements, or if the creation of
    fields and methods would result in other class attributes being
    overwritten.
    """
    pass
