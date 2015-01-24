import pytest
import os
import yaml

from photoshell.config import Config


@pytest.fixture
def config(tmpdir):
    return {
        'dark_theme': True,
        'import_path': '%Y-%m-%d/{original_filename}',
        'library': tmpdir.mkdir('library').strpath,
    }


def test_init_default_config(config):
    c = Config(initialdata=config, path='')
    assert c == config


def test_load(tmpdir, config):
    tmpdir.join('config.yml').write(yaml.dump(config,
                                              default_flow_style=False))
    c = Config(path=os.path.join(tmpdir.strpath, 'config.yml'))
    assert c == config


def test_flush(tmpdir, config):
    tmpdir.join('config.yml').write("")
    config_path = os.path.join(tmpdir.strpath, 'config.yml')
    c = Config(initialdata=config,
               path=config_path)
    c.flush()
    c2 = Config(path=config_path)
    assert c2 == config


def test_exists(tmpdir, config):
    tmpdir.join('config.yml').write("")
    config_path = os.path.join(tmpdir.strpath, 'config.yml')
    c = Config(initialdata=config,
               path=config_path)
    c2 = Config(initialdata=config,
                path=os.path.join(tmpdir.strpath, 'notconfig.yml'))

    assert c.exists() is True
    assert c2.exists() is False
