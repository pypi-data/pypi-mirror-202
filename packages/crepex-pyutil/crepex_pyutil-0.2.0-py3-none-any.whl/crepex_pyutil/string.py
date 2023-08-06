import base64
from urllib.parse import quote


def masking_string(target, location=1):
    if target.__len__() == location:
        return "*" * location
    return target[:location] + "*" + target[location + 1 :]


def string_to_base64(target, to_string=True):
    """
    문자열을 base64 형식으로 변환
    :param target: 변환대상
    :param to_string: 문자열 반환여부, False인 경우 bytes 반환
    """
    code = base64.b64encode(target.encode("utf-8"))
    if to_string:
        return code.decode("utf-8")
    return code


def base64_to_string(target: str):
    """
    base64 문자열을 decode 한 문자열 반환
    """
    return base64.b64decode(target).decode("utf-8")


def number_with_commas(number: int) -> str:
    return "{:,}".format(number)


def url_encode(value: str, encode="utf-8"):
    return quote(value, encode)


def is_mobile_number(value: str) -> bool:
    """
    휴대폰 번호 여부 체크
    """
    return value and value[:2] == "01"


def parse_tel(value) -> str:
    """
    전화번호 문자열에서 "-" 제거한 문자열 반환
    """
    raw = "" if type(value) != str else value
    return raw.replace("-", "")


def snake_to_camel(value: str) -> str:
    combined = value.split("_")
    return combined[0] + "".join(x.title() for x in combined[1:])
