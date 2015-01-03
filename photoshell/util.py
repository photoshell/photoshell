# TODO: murder this file, it will become a terrible catch all if it lives
import hashlib


def tuple_to_dict(t):
    """Convert a named tuple to a dict"""
    return dict(zip(t._fields, t))


def dict_to_tuple(cls, d):
    """Convert a dict to a named tuple"""
    fields = [d.get(field, '') for field in cls._fields]
    return cls(*fields)


# TODO: this shouldn't live on self
def hash_file(file_path):
    hash = hashlib.sha1()

    # TODO: probably block size or something, although if your machine
    # can't hold the whole file in memory you probably can't edit it
    # anyway.
    with open(file_path, 'rb') as f:
        data = f.read()

    hash.update(data)
    return hash.hexdigest()


class Progress(object):

    def __init__(self, num_to_complete):
        super(Progress, self).__init__()
        self.num_to_complete = num_to_complete
        self.num_complete = 0

    def advance(self):
        self.num_complete += 1
        return self.num_complete / self.num_to_complete
