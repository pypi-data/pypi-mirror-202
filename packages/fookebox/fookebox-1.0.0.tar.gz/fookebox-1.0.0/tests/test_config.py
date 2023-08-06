"""
Test the configuration loader.

The loader is responsible for loading the fookebox configuration file and for
providing reasonable default values.
"""
from fookebox.config import load_config, default_config


class TestConfigLoader:
    # pylint: disable=missing-class-docstring
    def test_load_empty_config(self):
        """Load an empty configuration file. All values should be set."""
        cfg = load_config('tests/fixtures/config-empty.ini')

        assert cfg.get('site_name') == "fookebox"
        assert cfg.getint('listen_port') == 8888
        assert cfg.get('mpd_host') == "localhost"
        assert cfg.getint('mpd_port') == 6600
        assert cfg.get('mpd_pass') is None
        assert cfg.getint('max_queue_length') == 5
        assert cfg.getboolean('auto_queue') is True
        assert cfg.getint('auto_queue_time_left') == 3
        assert cfg.get('auto_queue_playlist') is None
        assert cfg.get('auto_queue_genre') is None
        assert cfg.getboolean('show_search') is True
        assert cfg.getboolean('enable_controls') is True
        assert cfg.getboolean('enable_song_removal') is True
        assert cfg.getboolean('enable_queue_album') is True

    def test_load_config_without_fookebox_section(self):
        """Load a configuration file without a fookebox section.
           All values should be set."""
        cfg = load_config('tests/fixtures/config-no-fookebox-section.ini')

        assert cfg.get('site_name') == "fookebox"
        assert cfg.getint('listen_port') == 8888
        assert cfg.get('mpd_host') == "localhost"
        assert cfg.getint('mpd_port') == 6600
        assert cfg.get('mpd_pass') is None
        assert cfg.getint('max_queue_length') == 5
        assert cfg.getboolean('auto_queue') is True
        assert cfg.getint('auto_queue_time_left') == 3
        assert cfg.get('auto_queue_playlist') is None
        assert cfg.get('auto_queue_genre') is None
        assert cfg.getboolean('show_search') is True
        assert cfg.getboolean('enable_controls') is True
        assert cfg.getboolean('enable_song_removal') is True
        assert cfg.getboolean('enable_queue_album') is True

    def test_load_default_config(self):
        """Load default settings"""
        cfg = default_config()

        assert cfg.get('site_name') == "fookebox"
        assert cfg.getint('listen_port') == 8888
        assert cfg.get('mpd_host') == "localhost"
        assert cfg.getint('mpd_port') == 6600
        assert cfg.get('mpd_pass') is None
        assert cfg.getint('max_queue_length') == 5
        assert cfg.getboolean('auto_queue') is True
        assert cfg.getint('auto_queue_time_left') == 3
        assert cfg.get('auto_queue_playlist') is None
        assert cfg.get('auto_queue_genre') is None
        assert cfg.getboolean('show_search') is True
        assert cfg.getboolean('enable_controls') is True
        assert cfg.getboolean('enable_song_removal') is True
        assert cfg.getboolean('enable_queue_album') is True

    def test_load_some_config(self):
        """Load a configuration file. All values should be set."""
        cfg = load_config('tests/fixtures/config-example-1.ini')

        assert cfg.get('site_name') == "test site 1"
        assert cfg.getint('listen_port') == 8889
        assert cfg.get('mpd_host') == "test host"
        assert cfg.getint('mpd_port') == 612
        assert cfg.get('mpd_pass') == "test password"
        assert cfg.getint('max_queue_length') == 7
        assert cfg.getboolean('auto_queue') is True
        assert cfg.getint('auto_queue_time_left') == 19
        assert cfg.get('auto_queue_playlist') == "idle"
        assert cfg.get('auto_queue_genre') == "Jazz"
        assert cfg.getboolean('show_search') is True
        assert cfg.getboolean('enable_controls') is True
        assert cfg.getboolean('enable_song_removal') is True
        assert cfg.getboolean('enable_queue_album') is True

    def test_load_other_config(self):
        """Load a different configuration file. All values should be set."""
        cfg = load_config('tests/fixtures/config-example-2.ini')

        assert cfg.get('site_name') == "test site 2"
        assert cfg.getint('listen_port') == 8890
        assert cfg.get('mpd_host') == "mpd host"
        assert cfg.getint('mpd_port') == 613
        assert cfg.get('mpd_pass') == "password"
        assert cfg.getint('max_queue_length') == 6
        assert cfg.getboolean('auto_queue') is False
        assert cfg.getint('auto_queue_time_left') == 20
        assert cfg.get('auto_queue_playlist') == "playlist"
        assert cfg.get('auto_queue_genre') == "Rock & Roll"
        assert cfg.getboolean('show_search') is False
        assert cfg.getboolean('enable_controls') is False
        assert cfg.getboolean('enable_song_removal') is False
        assert cfg.getboolean('enable_queue_album') is False
