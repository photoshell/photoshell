import pytest

from photoshell.selection import Selection


@pytest.fixture
def sidecar():
    return {
        'developed_path': 'test.jpeg',
        'datetime': '2014-10-10 00:00'
    }


@pytest.fixture
def empty_selection():
    s = Selection('', '')
    return s


@pytest.fixture
def selection(empty_selection, sidecar):
    empty_selection.append(sidecar)
    return empty_selection


def test_append(empty_selection, sidecar):
    empty_selection.append(sidecar)
    assert empty_selection.photos[0] == sidecar


def test_current_photo_default_selection(selection):
    assert selection.current_photo()


def test_current_photo_is_none_if_selection_empty(empty_selection):
    assert empty_selection.current_photo() is None


def test_next_prev_does_nothing_single_photo(selection):
    assert selection.current_photo() == selection.next_photo()
    assert selection.current_photo() == selection.prev_photo()


def test_next_prev_wrap_around(empty_selection, sidecar):
    sidecar2 = {'datetime': 'datetime'}
    empty_selection.photos.append(sidecar)
    empty_selection.photos.append(sidecar2)

    assert empty_selection.next_photo() == sidecar2
    assert empty_selection.next_photo() == sidecar
    assert empty_selection.prev_photo() == sidecar2
    assert empty_selection.prev_photo() == sidecar
