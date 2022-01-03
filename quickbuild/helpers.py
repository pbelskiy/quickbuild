from enum import Enum
from typing import Any
from xml.parsers.expat import ExpatError

import xmltodict

CLASS_KEYWORD = '@class'


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
        # let's suppose it could be an XML document
        obj = xmltodict.parse(obj)
    except ExpatError:
        pass

    # case №1 - some primitive, like integer
    if isinstance(obj, dict) is False:
        return _to_python(obj)

    # case №2 - one object
    if 'list' not in obj:
        key = next(iter(obj))
        new_obj = obj[key]
        new_obj[CLASS_KEYWORD] = key
        return _to_python(new_obj)

    # case №3 - list of objects
    obj = obj['list']
    if obj is None:
        return []

    return _to_python(obj, to_list=True)


def _to_python(obj: Any, to_list: bool = False) -> Any:
    # pylint: disable=R0912

    if isinstance(obj, str):
        if obj.isdigit():
            return int(obj)

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = _to_python(v)
        return obj

    if isinstance(obj, dict) is False:
        return obj

    if list(obj.keys())[0].startswith('com.pmease.quickbuild') or to_list:
        new_obj = []

        for k, v in obj.items():
            if isinstance(v, list):
                for item in v:
                    item = _to_python(item)
                    if isinstance(item, dict):
                        item[CLASS_KEYWORD] = k
                    new_obj.append(_to_python(item))
            elif isinstance(v, dict):
                v[CLASS_KEYWORD] = k
                new_obj.append(_to_python(v))
            else:
                new_obj.append(_to_python(v))

        return new_obj

    orig, obj = obj, {}

    for k, v in orig.items():
        # make more json similar
        if k.startswith('@') and k != CLASS_KEYWORD:
            k = k[1:]

        if isinstance(v, (dict, list)):
            obj[k] = _to_python(v)
        elif isinstance(v, str) is False:
            obj[k] = v
            continue
        elif v == 'true':
            obj[k] = True
        elif v == 'false':
            obj[k] = False
        elif v.isdigit():
            obj[k] = int(v)
        else:
            obj[k] = v

    return obj
