from enum import Enum
from typing import Any
from xml.parsers.expat import ExpatError

import xmltodict


class ContentType(Enum):
    """
    - PARSE: get XML and parse it to native Python types
    - XML: get and post native XML documents
    - JSON: get and post native JSON documents (QuickBuild 10+)
    """
    PARSE = 1
    XML = 2
    JSON = 3

    _DEFAULT = PARSE


def response2py(obj: Any, content_type: ContentType) -> Any:
    """
    Smart and heuristic response converter to native python types.

    It`s much more convenient to work with native types instead of parsed XML
    which in strings inside. Also the main goal is to be equal with native json
    response from QuickBuild when used to be consistend in different versions.
    """
    if content_type == content_type.XML:
        return obj

    if obj == '':
        return None

    try:
        parsed = xmltodict.parse(obj)  # let's suppose it could be a XML document
    except ExpatError:
        parsed = obj
    else:
        if content_type == ContentType.XML:
            return obj

    # case №1 - some primitive, like integer
    if isinstance(parsed, dict) is False:
        return _to_python(parsed)

    # case №2 - one object
    if 'list' not in parsed:
        return _to_python(parsed[next(iter(parsed))])

    # case №3 - list of objects
    parsed = parsed['list']
    if parsed is None:
        return []

    parsed = parsed[next(iter(parsed))]
    if isinstance(parsed, list) is False:
        return [_to_python(parsed)]

    return _to_python(parsed)


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
