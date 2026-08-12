import json

from gleam_builtins import EmptyGleamList, Error, GleamList, Ok


def json_to_string(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def object(entries):
    result = {}
    head = entries
    while isinstance(head, GleamList):
        key, value = head.value
        result[key] = value
        head = head.tail
    return result


def identity(x):
    return x


def array(values):
    result = []
    head = values
    while isinstance(head, GleamList):
        result.append(head.value)
        head = head.tail
    return result


def do_null():
    return None


def decode(string):
    from gleam.json import UnexpectedByte, UnexpectedEndOfInput

    try:
        return Ok(_to_gleam(json.loads(string)))
    except json.JSONDecodeError as error:
        if error.pos >= len(error.doc):
            return Error(UnexpectedEndOfInput())
        return Error(UnexpectedByte(_to_hex_byte(error)))


def _to_gleam(value):
    if isinstance(value, list):
        result = EmptyGleamList()
        for item in reversed(value):
            result = GleamList(_to_gleam(item), result)
        return result
    return value


def _to_hex_byte(error):
    if error.msg.startswith("Invalid \\uXXXX escape"):
        return "0x78"
    return "0x" + format(ord(error.doc[error.pos]), "X")
