import hashlib


def hash_file(file_path):
    hash = hashlib.sha1()

    # TODO: probably block size or something, although if your machine
    # can't hold the whole file in memory you probably can't edit it
    # anyway.
    with open(file_path, 'rb') as f:
        data = f.read()

    hash.update(data)
    return hash.hexdigest()
