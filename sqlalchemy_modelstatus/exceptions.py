# -*- encoding: utf-8 -*-

class StatusTransitionException(Exception):
    def __init__(self, message, from_status=None, to_status=None):
        super(StatusTransitionException, self).__init__(message)
        self.from_status = from_status
        self.to_status = to_status

    def __repr__(self):
        inv_trans_str = "\nTransition from {} to {} is invalid." \
                        if self.from_status and self.to_status \
                        else ""
        return "{}{}".format(self.message, inv_trans_str)
