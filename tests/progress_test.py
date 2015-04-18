from photoshell.progress import Progress


def test_behavior_defaults():
    p = Progress()

    assert p.num_to_complete == 100


def test_behavior_advance():
    p = Progress()
    p.advance()

    assert p.num_complete == 1


def test_behavior_percent():
    p = Progress(200)
    p.advance()

    assert p.percent() == 0.005
