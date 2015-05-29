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
