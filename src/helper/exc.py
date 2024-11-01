def fail(exc: Exception):
    raise exc


class BaseApplicationException(Exception):
    pass
