import pytest

from photoshell.selection import Selection


@pytest.fixture
def sidecar():
    return {
        'developed_path': 'test.jpeg',
        'datetime': '2014-10-10 00:00'
    }


@pytest.fixture
def selection():
    s = Selection('')
    return s


def test_append(selection, sidecar):
    selection.append(sidecar)
    assert selection.photos[0] == sidecar


def test_current_photo_default_selection(selection, sidecar):
    selection.append(sidecar)
    assert selection.current_photo()


def test_current_photo_is_none_if_selection_empty(selection):
    assert selection.current_photo() is None


def test_next_prev_does_nothing_single_photo(selection, sidecar):
    selection.append(sidecar)
    assert selection.current_photo() == selection.next_photo()
    assert selection.current_photo() == selection.prev_photo()


def test_next_prev_wrap_around(selection, sidecar):
    sidecar2 = {'datetime': 'datetime'}
    selection.photos.append(sidecar)
    selection.photos.append(sidecar2)

    assert selection.next_photo() == sidecar2
    assert selection.next_photo() == sidecar
    assert selection.prev_photo() == sidecar2
    assert selection.prev_photo() == sidecar


def test_photo_generator(selection, sidecar):
    sidecar2 = "Pretend I'm a sidecar"
    selection.append(sidecar)
    selection.append(sidecar2)
    assert list(selection.each_photo()) == [sidecar, sidecar2]


def test_sort(selection, sidecar):
    sidecar2 = {'datetime': "0"}
    selection.append(sidecar)
    selection.append(sidecar2)
    selection.sort(key=lambda selection: selection['datetime'])
    assert list(selection.each_photo()) == [sidecar2, sidecar]
