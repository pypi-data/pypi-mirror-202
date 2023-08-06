import hashlib


def to_md5(obj):
    h = hashlib.md5()
    if isinstance(obj, bytes):
        h.update(obj)
    elif isinstance(obj, str):
        h.update(obj.encode('utf-8'))
    else:
        raise ValueError('Unsupported type: ' + str(type(obj)))
    return str(h.hexdigest()).upper()


def get_md5(text: str):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    v = m.hexdigest()
    return v
