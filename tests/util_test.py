import os

from photoshell import util


def test_hash_file(tmpdir):
    tmpdir.join('file.test').write("Test")
    assert (util.hash_file(os.path.join(tmpdir.strpath, 'file.test')) ==
            '640ab2bae07bedc4c163f679a746f7ab7fb5d1fa')
