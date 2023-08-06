"""
Test the page template. Make sure it handles translations and configuration
settings correctly.
"""
from importlib import resources

from bs4 import BeautifulSoup
from tornado import locale
from tornado.template import Template

import fookebox

from tests.common import ConfigWrapper


def _load_resource(dir_, filename):
    res = resources.files(fookebox).joinpath(dir_)
    with resources.as_file(res) as path:
        src = resources.files(fookebox).joinpath(path).joinpath(filename)
        with resources.as_file(src) as path:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()


class MockLocale:
    # pylint: disable=too-few-public-methods
    """
    This class is used as a basic no-op locale mock in tests where the locale
    does not matter.
    """
    def __init__(self, code="xx"):
        self.code = code

    def translate(self, val):
        # pylint: disable=missing-function-docstring
        return val


class TestTemplate:
    """
    Here we test the page template. The template can show/hide different
    controls based on the configuration.
    """
    def render(self, *, cfg, loc=MockLocale(), artists=None, genres=None):
        """Render the page template. This is used by other tests"""
        markup = _load_resource('templates', 'client.html')
        template = Template(markup)

        artists = artists or []
        genres = genres or []

        html = template.generate(config=cfg, locale=loc, artists=artists,
                                 genres=genres)
        return BeautifulSoup(html, 'html.parser')

    def test_show_search(self):
        """Show the search form if 'show_search' has been enabled"""
        config = ConfigWrapper()
        config.set('show_search', True)
        soup = self.render(cfg=config)

        assert soup.find("form", {"id": "artistSearchForm"}) is not None
        assert soup.find("form", {"id": "genreSearchForm"}) is not None

    def test_hide_search(self):
        """Hide the search form if 'show_search' has not been enabled"""
        config = ConfigWrapper()
        config.set('show_search', False)
        soup = self.render(cfg=config)

        assert soup.find("form", {"id": "artistSearchForm"}) is None
        assert soup.find("form", {"id": "genreSearchForm"}) is None

    def test_site_name(self):
        """Use the site_name as page title"""
        config = ConfigWrapper()
        config.set('site_name', 'test 51')
        soup = self.render(cfg=config)
        assert soup.find("title").text == "test 51"

        config.set('site_name', 'other test')
        soup = self.render(cfg=config)
        assert soup.find("title").text == "other test"

    def test_enable_controls(self):
        """Show the control panel controls have been enabled"""
        config = ConfigWrapper()
        config.set('enable_controls', True)
        soup = self.render(cfg=config)
        assert soup.find("div", {"id": "controls"}) is not None

    def test_disable_controls(self):
        """Hide the control panel controls have not been enabled"""
        config = ConfigWrapper()
        config.set('enable_controls', False)
        soup = self.render(cfg=config)
        assert soup.find("div", {"id": "controls"}) is None

    def test_locale_de(self):
        """Use the German translation"""
        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        soup = self.render(loc=locale.get('de'), cfg=ConfigWrapper())
        link = soup.find("a", {"id": "showArtists"})
        assert link.text == "Künstler"

    def test_locale_en(self):
        """Use the English language version"""
        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        soup = self.render(loc=locale.get('en'), cfg=ConfigWrapper())
        link = soup.find("a", {"id": "showArtists"})
        assert link.text == "Artists"

    def test_locale_fallback_unknown(self):
        """Use English as a fallback for unknown languages"""
        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        soup = self.render(loc=locale.get('fr'), cfg=ConfigWrapper())
        link = soup.find("a", {"id": "showArtists"})
        assert link.text == "Artists"

    def test_enable_song_removal(self):
        """Show the song removal links if song removal has been enabled"""
        config = ConfigWrapper()
        config.set('enable_song_removal', True)

        soup = self.render(cfg=config)
        queue = soup.find("ul", {"id": "queue"})
        assert queue.find("span", {"class": "controls"}) is not None

    def test_disable_song_removal(self):
        """Hide the song removal links if song removal has not been enabled"""
        config = ConfigWrapper()
        config.set('enable_song_removal', False)

        soup = self.render(cfg=config)
        queue = soup.find("ul", {"id": "queue"})
        assert queue.find("span", {"class": "controls"}) is None

    def test_disable_queue_album(self):
        """Show the links to queue whole albums if enabled"""
        config = ConfigWrapper()
        config.set('enable_queue_album', False)

        soup = self.render(cfg=config)
        body = soup.find("body")
        assert body.get("queue-albums") is None

    def test_enable_queue_album(self):
        """Hide the links to queue whole albums if not enabled"""
        config = ConfigWrapper()
        config.set('enable_queue_album', True)

        soup = self.render(cfg=config)
        body = soup.find("body")
        assert body.get("queue-albums") == "True"

    def test_artists(self):
        """Include the list of artists in the page"""
        soup = self.render(cfg=ConfigWrapper(), artists=['The KLF', 'Cher'])
        body = soup.find('body')
        assert len(body.find_all('li', {'class': 'artist'})) == 2

    def test_genres(self):
        """Include the list of genres in the page"""
        soup = self.render(cfg=ConfigWrapper(), genres=['Jazz', 'Funk', 'IDM'])
        body = soup.find('body')
        assert len(body.find_all('li', {'class': 'genre'})) == 3
