class QBError(Exception):
    """
    Core library exception
    """
    ...


class QBNotFoundError(QBError):
    """
    Raises when request return HTTP code 404 (not found)
    """
    ...
