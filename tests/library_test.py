import mock
import os
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


def test_library_creates_dir(config):
    config['library'] = os.path.join(config['library'], 'doesntexistyet')
    Library(config)

    assert(os.path.exists(config['library']))


def test_add(config, source_dir):
    library = Library(config)

    foo = Photo.create(
        raw_path=source_dir.join('foo.CR2'),
        file_hash='foo',
        developed_path=None,
    )
    bar = Photo.create(
        raw_path=source_dir.join('bar.CR2'),
        file_hash='bar',
        developed_path=None,
    )

    library.add(foo)

    assert library.exists(foo)
    assert not library.exists(bar)


def test_discover(config, source_dir):
    library = Library(config)

    with mock.patch('photoshell.library.hash_file', lambda f: f):
        progress, photo_iterator = library.discover(source_dir.strpath)
        photo_list = [photo for photo in photo_iterator()]

        # Make sure all the RAW files are accounted for.
        for raw_file in RAW_FILES:
            raw_path = source_dir.join(raw_file)
            assert raw_path in [p.raw_path for p in photo_list]

        # Add one of them to the library...
        library.add(photo_list[0])

        # And make sure the added file isn't discovered a second time.
        progress, photo_iterator = library.discover(source_dir.strpath)
        assert len([p for p in photo_iterator()]) == 2
        assert [photo for photo in photo_iterator()] == photo_list[1:]
