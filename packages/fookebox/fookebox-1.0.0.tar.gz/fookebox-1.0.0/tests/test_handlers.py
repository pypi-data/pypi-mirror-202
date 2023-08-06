"""
Test the request handlers

Notably, the handlers should
- accept any type of invalid data without raising any exceptions
- raise HTTP errors when invalid data is sent
- raise HTTP errors when a requested feature has been disabled
"""

from unittest.mock import Mock
from json import loads, dumps
from base64 import urlsafe_b64encode
from importlib import resources

from tornado import locale
from tornado.web import HTTPError
from bs4 import BeautifulSoup

import pytest

import fookebox
from fookebox.handlers import ArtistHandler, ControlHandler, CoverArtHandler
from fookebox.handlers import CSSHandler, FontHandler, GenreHandler
from fookebox.handlers import IndexHandler, JSHandler, QueueHandler
from fookebox.handlers import StatusHandler

from tests.common import ConfigWrapper, MockMPD


class TestStatusHandler:
    """
    Test the StatusHandler

    This handler has a single method:

    - GET allows the client to ask the server for the current status. The
      status includes the currently playing song as well as the length of the
      queue.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        app = Mock()

        self.mpd = MockMPD()
        self.handler = StatusHandler(request, app, mpd=self.mpd)

    def test_get_empty(self):
        # pylint: disable=protected-access
        """Get server status with empty queue and no song playing"""
        self.handler.get()
        data = loads(self.handler._write_buffer[0])

        assert "volume" in data
        assert data["volume"] == 0

        assert "queueLength" in data
        assert data["queueLength"] == 0

    def test_get_status_and_current_song(self):
        # pylint: disable=protected-access
        """Get server status with empty queue but a song playing"""
        self.mpd.mpd_status["pos"] = 0
        self.mpd.mpd_current_song = "song.flac"
        self.handler.get()
        data = loads(self.handler._write_buffer[0])

        assert data["volume"] == 0
        assert data["queueLength"] == 0
        assert data.get("file") == "song.flac"

    def test_get_status_with_nonempty_queue(self):
        # pylint: disable=protected-access
        """Get server status when the queue is not empty"""
        self.mpd.mpd_status["pos"] = 0
        self.mpd.mpd_current_song = "song.flac"
        self.mpd.mpd_queue = ["foo", "bar"]
        self.handler.get()
        data = loads(self.handler._write_buffer[0])

        assert data["volume"] == 0
        assert data["queueLength"] == 2
        assert data.get("file") == "song.flac"


class TestQueueHandler:
    """
    Test the QueueHandler

    This handler has two methods:

    - GET allows the client to load the current queue
    - POST accepts a JSON-encoded list of files to add to the queue

    The POST operation should respect the max_queue_length setting.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        app = Mock()

        self.mpd = MockMPD()
        self.config = ConfigWrapper()
        self.app = app
        self.handler = QueueHandler(request, app, mpd=self.mpd,
                                    cfg=self.config)

    def test_get_queue(self):
        # pylint: disable=protected-access
        """Get a queue with a bunch of files in there"""
        self.mpd.mpd_current_song = "f0"
        self.mpd.mpd_queue = ["f1", "f2", "f3"]

        self.handler.get()
        data = loads(self.handler._write_buffer[0])
        assert data == {"queue": ["f1", "f2", "f3"]}

    # pylint: disable=protected-access
    def test_get_queue_empty(self):
        """Get an empty queue"""
        self.handler.get()
        data = loads(self.handler._write_buffer[0])
        assert data == {"queue": []}

    def test_post_track(self):
        """Post a single track (the normal case)"""
        assert not self.mpd.mpd_queue
        assert len(self.mpd.commands) == 0

        self.app.body = dumps({"files": ["f1"]})
        self.handler.post()

        assert self.mpd.mpd_queue == ["f1"]
        assert len(self.mpd.commands) == 1
        assert self.mpd.commands[0] == "play"

    def test_post_multiple_tracks(self):
        """Post multiple tracks in a single request (eg. a whole album)"""
        assert len(self.mpd.commands) == 0

        self.mpd.mpd_current_song = "f1"
        self.app.body = dumps({"files": ["f2", "f3", "f4"]})
        self.handler.post()

        assert self.mpd.mpd_queue == ["f2", "f3", "f4"]
        assert len(self.mpd.commands) == 1
        assert self.mpd.commands[0] == "play"

    def test_post_track_queue_full(self):
        """Posting when the queue is full should raise a 409"""
        assert len(self.mpd.commands) == 0

        self.config.set('max_queue_length', 5)
        self.mpd.mpd_current_song = "f1"
        self.mpd.mpd_queue = ["f2"]

        self.app.body = dumps({"files": ["f3", "f4", "f5"]})
        self.handler.post()
        assert self.mpd.mpd_queue == ["f2", "f3", "f4", "f5"]

        self.app.body = dumps({"files": ["f6"]})
        self.handler.post()
        assert self.mpd.mpd_queue == ["f2", "f3", "f4", "f5", "f6"]

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.log_message == "Queue full"
        assert ctx.value.status_code == 409

        assert self.mpd.mpd_queue == ["f2", "f3", "f4", "f5", "f6"]

    def test_posting_too_many_tracks_fills_queue(self):
        """Posting too many songs should fill the queue and raise a 409"""
        self.config.set('max_queue_length', 5)
        self.mpd.mpd_current_song = "f1"

        files = ["f2", "f3", "f4", "f5", "f6", "f7", "f8"]
        self.app.body = dumps({'files': files})

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.log_message == "Queue full"
        assert ctx.value.status_code == 409

        assert self.mpd.mpd_queue == ["f2", "f3", "f4", "f5", "f6"]

    def test_post_invalid_data(self):
        """Accept (and ignore) requests with invalid data"""
        assert len(self.mpd.commands) == 0
        assert not self.mpd.mpd_queue

        self.app.body = dumps({"files": 12})

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.log_message == "Invalid data"
        assert ctx.value.status_code == 400

        assert not self.mpd.mpd_queue
        assert len(self.mpd.commands) == 0

    def test_post_invalid_json(self):
        """Accept (and ignore) requests with invalid JSON data"""
        assert len(self.mpd.commands) == 0
        assert not self.mpd.mpd_queue

        self.app.body = '{"files": 12'

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.log_message == "Invalid JSON data"
        assert ctx.value.status_code == 400

        assert not self.mpd.mpd_queue
        assert len(self.mpd.commands) == 0

    def test_post_missing_data(self):
        """Accept (and ignore) requests without any relevant data"""
        assert len(self.mpd.commands) == 0
        assert not self.mpd.mpd_queue

        self.app.body = dumps({"bla": 12})

        assert not self.mpd.mpd_queue
        assert len(self.mpd.commands) == 0

    def test_delete(self):
        """Delete a song from the queue"""
        self.config.set('enable_song_removal', True)
        self.mpd.mpd_queue = ["A", "B", "C", "D"]
        self.handler.delete(2)

        assert self.handler.get_status() == 200
        assert self.mpd.mpd_queue == ["A", "B", "D"]

    def test_delete_without_permission(self):
        """Raise a 403 error when song removal is not allowed"""
        self.config.set('enable_song_removal', False)
        self.mpd.mpd_queue = ["A", "B", "C", "D"]

        with pytest.raises(HTTPError) as ctx:
            self.handler.delete(2)

        assert ctx.value.status_code == 403
        assert self.mpd.mpd_queue == ["A", "B", "C", "D"]

    def test_delete_invalid_index(self):
        """Raise a 400 error when trying to delete an invalid index"""
        self.config.set('enable_song_removal', True)
        self.mpd.mpd_queue = ["A", "B", "C", "D"]

        with pytest.raises(HTTPError) as ctx:
            self.handler.delete(5)

        assert ctx.value.log_message == "Bad song index"
        assert ctx.value.status_code == 400
        assert self.mpd.mpd_queue == ["A", "B", "C", "D"]


class TestCoverArtHandler:
    """
    Test the CoverArtHandler

    The CoverArtHandler fetches album art for a specific file from mpd. It
    expects the file to be passed as a parameter in the URL.

    If cover art is disabled, the handler should raise an HTTP error instead.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        app = Mock()
        app.ui_methods = {}
        self.request = Mock()

        self.mpd = MockMPD()
        self.mpd.mpd_covers = {
            '/media/somebody - my song.mp3': 'blank.png',
            '/media/somebody - second song.mp3': 'blank.jpg'
        }
        self.config = ConfigWrapper()
        self.handler = CoverArtHandler(app, self.request, mpd=self.mpd,
                                       cfg=self.config)

    def test_get_cover_that_does_not_exist(self):
        """Report a 404 error if a cover is not available"""
        file = "/media/somebody - no song.mp3"

        with pytest.raises(HTTPError) as ctx:
            self.handler.get(file)
        assert ctx.value.status_code == 404

    def test_get_cover(self):
        # pylint: disable=protected-access
        """Load a cover image"""
        file = "/media/somebody - my song.mp3"
        self.handler.get(file)

        data = self.handler._write_buffer[0]
        encoded = urlsafe_b64encode(data)
        assert encoded.startswith(b'iVBOR')

    def test_get_cover_mime_type(self):
        # pylint: disable=protected-access
        """Get and report the correct mime type from a cover image"""
        file = "/media/somebody - my song.mp3"
        self.handler.get(file)

        headers = self.handler._headers
        assert headers["Content-Type"] == "image/png"

        file = "/media/somebody - second song.mp3"
        self.handler.get(file)

        headers = self.handler._headers
        assert headers["Content-Type"] == "image/jpeg"


class TestControlHandler:
    """
    Test the ControHandler

    The ControlHandler handles mpd commands such as 'play', 'pause' etc.

    These commands should be forwarded to the backend if controls are enabled
    in the configuration, otherwise the handler should throw an error.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        self.app = Mock()

        self.mpd = MockMPD()
        self.config = ConfigWrapper()
        self.handler = ControlHandler(request, self.app, mpd=self.mpd,
                                      cfg=self.config)

    def test_controls_disabled(self):
        """Commands should trigger an HTTP error if controls are disabled"""
        self.config.set('enable_controls', False)
        self.app.body = dumps({'action': 'play'})

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.status_code == 403

    def test_invalid_json(self):
        """Check that invalid JSON data triggers an HTTP error"""
        self.config.set('enable_controls', True)
        self.app.body = '{"action": "bogus"'

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.status_code == 400

    def test_missing_command(self):
        """Check that a request without a command triggers an HTTP error"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'foo': 'play'})

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.status_code == 400

    def test_invalid_command(self):
        """Check that invalid comands trigger an HTTP error"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'bogus'})

        with pytest.raises(HTTPError) as ctx:
            self.handler.post()
        assert ctx.value.status_code == 400

    def test_command_play(self):
        """Check that the 'play' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'play'})
        self.handler.post()

        assert self.mpd.commands == ['play']

    def test_command_pause(self):
        """Check that the 'pause' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'pause'})
        self.handler.post()

        assert self.mpd.commands == ['pause']

    def test_command_next(self):
        """Check that the 'next' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'next'})
        self.handler.post()

        assert self.mpd.commands == ['next']

    def test_command_prev(self):
        """Check that the 'prev' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'prev'})
        self.handler.post()

        assert self.mpd.commands == ['previous']

    def test_command_volup(self):
        """Check that the 'volume up' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'volup'})
        self.handler.post()

        assert self.mpd.commands == ['volume 10']

    def test_command_voldown(self):
        """Check that the 'volume down' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'voldown'})
        self.handler.post()

        assert self.mpd.commands == ['volume -10']

    def test_command_rebuild(self):
        """Check that the 'rebuild' command is sent to the backend"""
        self.config.set('enable_controls', True)
        self.app.body = dumps({'action': 'rebuild'})
        self.handler.post()

        assert self.mpd.commands == ['update']


class TestArtistHandler:
    """
    Test the ArtistHandler

    The artist handler searches MPD for songs by a certain artist and returns
    these songs.

    It should not choke on requests with invalid artist names.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        self.app = Mock()

        self.mpd = MockMPD()
        self.handler = ArtistHandler(request, self.app, mpd=self.mpd)
        self.mpd.mpd_files.append({'artist': 'The KLF', 'title': '001'})
        self.mpd.mpd_files.append({'artist': 'The KLF', 'title': '002'})
        self.mpd.mpd_files.append({'artist': 'The KLF', 'title': '003'})
        self.mpd.mpd_files.append({'artist': 'The Who', 'title': '004'})
        self.mpd.mpd_files.append({'artist': 'The Who', 'title': '005'})
        self.mpd.mpd_files.append({'artist': 'The The', 'title': '006'})

    def test_get_artist(self):
        """Get all files from a certain artist"""
        # pylint: disable=protected-access
        self.handler.get('The KLF')
        data = loads(self.handler._write_buffer[0])
        tracks = data['tracks']

        assert isinstance(tracks, list)
        assert len(tracks) == 3

        for track in tracks:
            assert track['artist'] == 'The KLF'

    def test_get_artist_with_no_files(self):
        """Get all files from an artist that has no files. Should be empty."""
        # pylint: disable=protected-access
        self.handler.get('Eels')
        data = loads(self.handler._write_buffer[0])
        tracks = data['tracks']

        assert isinstance(tracks, list)
        assert len(tracks) == 0


class TestGenreHandler:
    """
    Test the GenreHandler

    The genre handler searches MPD for songs from a certain genre and returns
    these songs.

    It should not choke on requests with invalid genres.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        self.app = Mock()

        self.mpd = MockMPD()
        self.handler = GenreHandler(request, self.app, mpd=self.mpd)
        self.mpd.mpd_files.append({'genre': 'Electro', 'title': '001'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'title': '002'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'title': '003'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'title': '004'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'title': '005'})
        self.mpd.mpd_files.append({'genre': 'Pop', 'title': '006'})

    def test_get_genre(self):
        """Get all files from a certain genre"""
        # pylint: disable=protected-access
        self.handler.get('Jazz')
        data = loads(self.handler._write_buffer[0])
        tracks = data['tracks']

        assert isinstance(tracks, list)
        assert len(tracks) == 2

        for track in tracks:
            assert track['genre'] == 'Jazz'

    def test_get_genre_with_no_files(self):
        """Get all files from a genre that has no files. Should be empty."""
        # pylint: disable=protected-access
        self.handler.get('Rap')
        data = loads(self.handler._write_buffer[0])
        tracks = data['tracks']

        assert isinstance(tracks, list)
        assert len(tracks) == 0


class TestCSSHandler:
    """
    Test the CSSHandler

    The CSS handler serves (static) CSS files from the package resources.

    It should return the CSS file if it's there, or a 404 error otherwise.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        app = Mock()

        self.handler = CSSHandler(request, app)

    def test_get_css(self):
        """Get a CSS file"""
        # pylint: disable=protected-access
        self.handler.get('fookebox.css')
        data = self.handler._write_buffer[0]
        assert data[:4] == b'body'

    def test_get_invalid_css(self):
        """Raise a 404 error if the CSS file cannot be found"""
        with pytest.raises(HTTPError) as ctx:
            self.handler.get('no-such-file.css')

        assert ctx.value.status_code == 404


class TestFontHandler:
    """
    Test the FontHandler

    The font handler serves (static) font files from the package resources.

    It should return the font if it's there, or a 404 error otherwise.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        app = Mock()

        self.handler = FontHandler(request, app)

    def test_get_svg_font(self):
        """Get a font file"""
        # pylint: disable=protected-access
        self.handler.get('glyphicons-halflings-regular.svg')
        data = self.handler._write_buffer[0]
        assert data[:5] == b'<?xml'

        headers = self.handler._headers
        assert headers["Content-Type"] == 'image/svg+xml'

    def test_get_binary_font(self):
        """Get a font file"""
        # pylint: disable=protected-access
        self.handler.get('glyphicons-halflings-regular.ttf')
        data = self.handler._write_buffer[0]
        assert data is not None

        headers = self.handler._headers
        assert headers["Content-Type"] == 'font/sfnt'

    def test_get_invalid_font(self):
        """Raise a 404 error if the font cannot be found"""
        with pytest.raises(HTTPError) as ctx:
            self.handler.get('no-such-file.ttf')

        assert ctx.value.status_code == 404


class TestJSHandler:
    """
    Test the JSHandler

    The JS handler serves (static) JavaScript files from the package resources.

    It should return the script file if it's there, or a 404 error otherwise.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        request = Mock()
        request.ui_methods = {}
        app = Mock()

        self.handler = JSHandler(request, app)

    def test_get_js(self):
        """Get a font file"""
        # pylint: disable=protected-access
        self.handler.get('fookebox.js')
        data = self.handler._write_buffer[0]
        assert data[:12] == b'"use strict"'

    def test_get_invalid_js(self):
        """Raise a 404 error if the font cannot be found"""
        with pytest.raises(HTTPError) as ctx:
            self.handler.get('no-such-file.js')

        assert ctx.value.status_code == 404


class TestIndexHandler:
    """
    Test the IndexHandler

    The index handler is responsible for loading the HTML tempalte, filling in
    the artists and genres and loading the appropriate language.
    """
    def setup_method(self):
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=missing-function-docstring
        self.request = Mock()
        self.request.headers = {}
        app = Mock()
        app.ui_methods = {}

        self.mpd = MockMPD()
        self.mpd.mpd_files.append({'genre': 'Electro', 'artist': 'A01'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'artist': 'A02'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'artist': 'A02'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'artist': 'A01'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'artist': 'A03'})
        self.mpd.mpd_files.append({'genre': 'Pop', 'artist': 'A04'})

        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        cfg = ConfigWrapper()
        self.handler = IndexHandler(app, self.request, mpd=self.mpd, cfg=cfg)

    def test_get_index(self):
        # pylint: disable=protected-access
        """Load the HTML template"""
        self.handler.get()
        data = self.handler._write_buffer[0]
        assert data[:9] == b'<!DOCTYPE'

    def test_index_contains_artists_and_genres(self):
        # pylint: disable=protected-access
        """Check that the template contains all artists and genres"""
        self.handler.get()
        data = self.handler._write_buffer[0]
        soup = BeautifulSoup(data, 'html.parser')

        artists = soup.find_all('li', {'class': 'artist'})
        assert len(artists) == 4

        genres = soup.find_all('li', {'class': 'genre'})
        assert len(genres) == 3

    def test_index_uses_english_language_by_default(self):
        # pylint: disable=protected-access
        """If no language has been specified, the page should be in English"""
        self.handler.get()
        data = self.handler._write_buffer[0]
        soup = BeautifulSoup(data, 'html.parser')

        artists = soup.find('a', {'id': 'showArtists'})
        assert artists.text == 'Artists'

    def test_index_uses_german_if_requested(self):
        # pylint: disable=protected-access
        """If the browser wants the page in German, we obey"""
        self.request.headers['Accept-Language'] = 'de'
        self.handler.get()
        data = self.handler._write_buffer[0]
        soup = BeautifulSoup(data, 'html.parser')

        artists = soup.find('a', {'id': 'showArtists'})
        assert artists.text == 'Künstler'

    def test_index_falls_back_to_english(self):
        # pylint: disable=protected-access
        """If the browser wants the page in Italian, we use English instead"""
        self.request.headers['Accept-Language'] = 'it'
        self.handler.get()
        data = self.handler._write_buffer[0]
        soup = BeautifulSoup(data, 'html.parser')

        artists = soup.find('a', {'id': 'showArtists'})
        assert artists.text == 'Artists'
