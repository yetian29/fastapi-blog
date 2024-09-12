def fail(exc: Exception):
    raise exc


class BaseDomainException(Exception):
    pass


class BaseServiceException(Exception):
    pass