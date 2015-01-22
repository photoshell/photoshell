import mock
import pytest

from photoshell.library import Library
from photoshell.photo import Photo


RAW_FILES = ['foo.CR2', 'bar.CR2', 'baz.CR2']


@pytest.fixture
def config(tmpdir):
    return {
        'dark_theme': True,
        'import_path': '%Y-%m-%d/{original_filename}',
        'library': tmpdir.mkdir('library').strpath,
    }


@pytest.fixture
def source_dir(tmpdir):
    source = tmpdir.mkdir('source')

    for f in RAW_FILES:
        source.join(f).ensure(file=True)

    return source


def create_photo(raw_path, file_hash=None):

    return Photo(
        None,  # aperture
        None,  # datetime
        None,  # developed_path
        None,  # exposure
        None,  # flash
        None,  # focal_length
        None,  # gps
        hash(raw_path),  # file_hash
        None,  # height
        None,  # iso
        None,  # lens
        None,  # make
        None,  # model
        None,  # orientation
        raw_path,  # raw_path
        None,  # width
    )


def test_add(config, source_dir):
    library = Library(config)

    foo = create_photo(source_dir.join('foo.CR2'))
    bar = create_photo(source_dir.join('bar.CR2'))

    library.add(foo)

    assert library.exists(foo)
    assert not library.exists(bar)


def test_discover(config, source_dir):
    library = Library(config)

    with mock.patch.object(Photo, 'load', create_photo):
        photo_count, photo_iterator = library.discover(source_dir.strpath)
        photo_list = [photo for photo in photo_iterator()]

        # Make sure all the RAW files are accounted for.
        for raw_file in RAW_FILES:
            raw_path = source_dir.join(raw_file)
            assert raw_path in [p.raw_path for p in photo_list]

        # Add one of them to the library...
        library.add(photo_list[0])

        # And make sure the added file isn't discovered a second time.
        photo_count, photo_iterator = library.discover(source_dir.strpath)
        assert photo_count == 2
        assert [photo for photo in photo_iterator()] == photo_list[1:]
