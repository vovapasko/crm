import base64

encoding = 'utf8'


def base64_encode(message: str) -> str:
    message_bytes = message.encode(encoding)
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode(encoding)
    return base64_message


def base64_decode(message: str) -> str:
    base64_bytes = message.encode(encoding)
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode(encoding)
    return message
