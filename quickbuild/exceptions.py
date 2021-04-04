class QBError(Exception):
    """
    Core library exception
    """
    ...


class QBProcessingError(QBError):
    """
    Raises when request return HTTP code 204 (no content)
    """
    ...


class QBForbiddenError(QBError):
    """
    Raises when request return HTTP code 403 (forbidden)
    """
    ...


class QBNotFoundError(QBError):
    """
    Raises when request return HTTP code 404 (not found)
    """
    ...
