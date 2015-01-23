import os

from photoshell.photo import Photo


def create_photo(file_hash, raw_path=None):
    return Photo(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        file_hash,
        None,
        None,
        None,
        None,
        None,
        None,
        raw_path,
        None,
    )


# def test_load(tmpdir):
#     photo_path = tmpdir.join('foo.CR2').ensure(file=True)
#     dt = datetime.now()
#
#     with mock.patch.object(raw, 'read_meta', return_value={'datetime': dt}):
#         photo = Photo.load(photo_path.strpath)
#
#         assert photo.raw_path == photo_path.strpath
#         assert photo.datetime == dt


def test_copy(tmpdir):
    photo_path = tmpdir.join('foo.CR2').ensure(file=True)

    new_photo_path = tmpdir.join('bar.CR2')
    new_sidecar_path = tmpdir.join('bar.CR2.yaml')

    photo = create_photo('foo', photo_path.strpath)

    new_photo = photo.copy(new_photo_path.strpath, delete_originals=False)
    assert new_photo.raw_path == new_photo_path
    assert new_photo.raw_path + '.yaml' == new_sidecar_path
    assert os.path.exists(new_photo_path.strpath)


def test_develop():
    pass


def test_equal():
    foo1 = create_photo('foo')
    foo2 = create_photo('foo')
    bar = create_photo('bar')

    assert foo1 == foo2
    assert foo1 != bar
