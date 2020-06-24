import time
import hashlib


def log(*args, **kwargs):
    print(*args, **kwargs)


def random_name():
    t = str(time.time())
    hl = hashlib.md5()
    hl.update(t.encode())
    name = '人工智障' + hl.hexdigest()[:4]
    return name
