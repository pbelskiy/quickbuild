from typing import Any
from xml.parsers.expat import ExpatError

import xmltodict


def response2py(obj: Any) -> Any:
    """
    Smart and heuristic response converter to native python types.

    It`s much more convenient to work with native types instead of parsed XML
    which in strings inside. Also the main goal is to be equal with native json
    response from QuickBuild when used to be consistend in different versions.
    """
    try:
        obj = xmltodict.parse(obj)  # let's suppose it could be a XML document
    except ExpatError:
        pass

    # case №1 - some primitive, like integer
    if isinstance(obj, dict) is False:
        return _to_python(obj)

    # case №2 - one object
    if 'list' not in obj:
        return _to_python(obj[next(iter(obj))])

    # case №3 - list of objects
    obj = obj['list']
    if obj is None:
        return []

    obj = obj[next(iter(obj))]
    if isinstance(obj, list) is False:
        return [_to_python(obj)]

    return _to_python(obj)


def _to_python(obj: Any) -> Any:
    if isinstance(obj, str):
        if obj.isdigit():
            return int(obj)

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = _to_python(v)
        return obj

    elif isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = _to_python(v)
            elif isinstance(v, str) is False:
                continue
            elif v == 'true':
                obj[k] = True
            elif v == 'false':
                obj[k] = False
            elif v.isdigit():
                obj[k] = int(v)

    return obj
