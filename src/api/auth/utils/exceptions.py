class AccountAlreadyRegistred(Exception):
    pass


class AccountAlreadyConfirmed(Exception):
    pass


class AccountNotConfirmed(Exception):
    pass


class IvalidInviteToken(Exception):
    pass


class InvalidEmailOrPassword(Exception):
    pass
