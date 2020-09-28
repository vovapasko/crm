import base64

encoding = 'utf8'


def base64_encode(text: str) -> str:
    return base64.encodebytes(bytes(text, encoding=encoding))


def base64_decode(text: bytes) -> str:
    return str(base64.decodebytes(text).decode(encoding))
