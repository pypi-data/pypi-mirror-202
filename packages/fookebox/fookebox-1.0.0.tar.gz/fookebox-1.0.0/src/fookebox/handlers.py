# fookebox, https://code.ott.net/fookebox/
# Copyright (c) 2007-2023 Stefan Ott. all rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module contains all of fookbox's RequestHandlers.
"""

from configparser import SectionProxy
from importlib import resources
import json

import magic
from mpd.base import CommandError
from tornado import template
from tornado.web import HTTPError, RequestHandler

import fookebox
from .mpd import MPDContext


class ArtistHandler(RequestHandler):
    """
    A RequestHandler to load tracks by a particular artist.

    Methods
    -------
    get(artist):
        Load tracks of by particular artist.
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext):
        """Initialize the ArtistHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd

    def get(self, artist: str):
        """
        Returns tracks by a particular artist.

        Parameters
        ----------
        artist : str
            name of the artist

        Returns
        -------
        A list of tracks by the specified artist, wrapped in a dictionary under
        the 'tracks' key.
        """
        with self._mpd as client:
            hits = client.find('artist', artist)

        self.write({'tracks': hits})


class GenreHandler(RequestHandler):
    """
    A RequestHandler to load tracks of a particular genre.

    Methods
    -------
    get(genre):
        Load tracks of a particular genre.
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext):
        """Initialize the GenreHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd

    def get(self, genre: str):
        """
        Returns tracks from a particular genre.

        Parameters
        ----------
        genre : str
            name of the genre

        Returns
        -------
        A list of tracks from the specified genre, wrapped in a dictionary
        under the 'tracks' key.
        """
        with self._mpd as client:
            hits = client.find('genre', genre)

        self.write({'tracks': hits})


class ControlHandler(RequestHandler):
    """
    A RequestHandler to control MPD.

    This handler allows clients to send commands such as play, pause etc. to
    MPD.

    Methods
    -------
    post():
        Send a command to MPD
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext, cfg: SectionProxy):
        """Initialize the ControlHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd
        self._cfg = cfg

    def post(self):
        """
        Send a command to MPD

        A JSON-encoded dictionary with the keyword 'action' and the MPD command
        as a value is expected in the POST body. Something like this:

            {'action': 'play'}

        Valid commands are play, pause, next, prev, volup, voldown and rebuild.

        Whether or not clients are allowed to send MPD commands can be
        configured using the 'enable_controls' config option.

        Returns
        -------
        This method does not return anything.

        Exceptions
        ----------
        - If controls have been disabled, a HTTP 403 error is raised.
        - If the supplied JSON data is invalid, a HTTP 400 error is raised.
        - If an unknown command has been sent, a HTTP 400 error is raised.
        """
        if not self._cfg.getboolean('enable_controls'):
            raise HTTPError(403, 'Controls disabled')

        try:
            data = json.loads(self.request.body)
        except json.decoder.JSONDecodeError as exc:
            raise HTTPError(400, 'Invalid JSON data') from exc

        commands = {
            'next': lambda client: client.next(),
            'prev': lambda client: client.previous(),
            'play': lambda client: client.play(),
            'pause': lambda client: client.pause(),
            'volup': lambda client: client.volume(+10),
            'voldown': lambda client: client.volume(-10),
            'rebuild': lambda client: client.update()
        }

        action = data.get('action')
        if action not in commands:
            raise HTTPError(400, 'Invalid command')

        with self._mpd as client:
            commands[action](client)


class CoverArtHandler(RequestHandler):
    """
    A RequestHandler that serves cover art.

    Methods
    -------
    get(filename):
        Get cover art for a file
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext, cfg: SectionProxy):
        """Initialize the CoverArtHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd
        self._cfg = cfg

    def get(self, filename: str):
        """
        Returns cover art for a particular file.

        Parameters
        ----------
        filename : str
            name of the file

        Returns
        -------
        Cover art for the specified file name.

        Exceptions
        ----------
        If no cover art is found, a HTTP 404 error is raised
        """
        with self._mpd as client:
            try:
                albumart = client.albumart(filename)
            except CommandError as exc:
                raise HTTPError(404, 'Cover art not found') from exc

        data = albumart['binary']
        mime = magic.from_buffer(data, mime=True)

        self.write(data)
        self.set_header('content-type', mime)


def _read_resource(dir_, filename):
    src = resources.files(fookebox).joinpath(dir_).joinpath(filename)
    with resources.as_file(src) as path:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()


def _read_binary_resource(dir_, filename):
    src = resources.files(fookebox).joinpath(dir_).joinpath(filename)
    with resources.as_file(src) as path:
        with open(path, 'rb') as file:
            return file.read()


class CSSHandler(RequestHandler):
    """A RequestHandler that serves CSS files from the package resources."""
    # pylint: disable=abstract-method
    def get(self, filename: str):
        """
        Get the a CSS file from the package resources.

        Parameters
        ----------
        filename : str
            name of the file
        """
        try:
            data = _read_resource('css', filename)
        except FileNotFoundError as exc:
            raise HTTPError(404) from exc

        self.set_header('content-type', 'text/css')
        self.write(data)


class FontHandler(RequestHandler):
    """A RequestHandler that serves fonts from the package resources."""
    # pylint: disable=abstract-method
    def get(self, filename: str):
        """
        Get the a font from the package resources.

        Parameters
        ----------
        filename : str
            name of the font file
        """
        try:
            data = _read_binary_resource('fonts', filename)
        except FileNotFoundError as exc:
            raise HTTPError(404) from exc

        mime = magic.from_buffer(data, mime=True)

        self.write(data)
        self.set_header('content-type', mime)


class IndexHandler(RequestHandler):
    """A RequestHandler that serves the index HTML file."""
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext, cfg: SectionProxy):
        """Initialize the IndexHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self.mpd = mpd
        self.cfg = cfg

    def get(self):
        """
        Load the index HTML file.

        The HTML file comes pre-loaded with all available artists and genres,
        rendered in the browser's preferred language (if available).
        """
        with self.mpd as client:
            artists = [x['artist'] for x in client.list('artist')]
            genres = [x['genre'] for x in client.list('genre')]

        markup = _read_resource('templates', 'client.html')
        tpl = template.Template(markup)
        output = tpl.generate(config=self.cfg, artists=artists, genres=genres,
                              locale=self.get_browser_locale())
        self.write(output)


class JSHandler(RequestHandler):
    """A RequestHandler that serves JavaScript from the package resources."""
    # pylint: disable=abstract-method
    def get(self, filename: str):
        """
        Get the a JavaScript file from the package resources.

        Parameters
        ----------
        filename : str
            name of the file
        """
        try:
            data = _read_resource('js', filename)
        except FileNotFoundError as exc:
            raise HTTPError(404) from exc

        self.set_header('content-type', 'text/javascript')
        self.write(data)


class QueueHandler(RequestHandler):
    # pylint: disable=abstract-method
    """
    A RequestHandler that allows clients to interact with MPD's queue.

    Methods
    -------
    get():
        Get the current queue
    post():
        Add an arbitrary number of tracks to the queue
    delete():
        Remove a track from the queue
    """
    def initialize(self, mpd: MPDContext, cfg: SectionProxy):
        # pylint: disable=attribute-defined-outside-init
        """Initialize the QueueHandler object"""
        self._mpd = mpd
        self._cfg = cfg

    def get(self):
        """
        Returns the currently queued tracks.

        This does not include the track that is being played at the moment.
        """
        with self._mpd as client:
            queue = client.playlistinfo()
            status = client.status()

        index = int(status.get('song', 0))
        self.write({'queue': queue[index+1:]})

    def post(self):
        """
        Add tracks to the queue.

        A JSON-encoded list of tracks to be added to the queue is read from the
        POST body. The tracks are then added, one by one, to the queue until
        there are no more tracks left or the queue is full.

        The queue size is determined from the max_queue_length configuration
        option.

        Returns
        -------
        This method does not return anything.

        Exceptions
        ----------
        - If the queue limit has been exceeded, a HTTP 409 error is raised.
        - If the supplied JSON data is invalid, a HTTP 400 error is raised.
        """
        try:
            data = json.loads(self.request.body)
        except json.decoder.JSONDecodeError as exc:
            raise HTTPError(400, 'Invalid JSON data') from exc

        dir_ = data.get('files', [])
        maxlen = self._cfg.getint('max_queue_length')

        if not isinstance(dir_, list):
            raise HTTPError(400, 'Invalid data')

        with self._mpd as client:
            for file in dir_:
                playlist = client.playlist()[1:]
                if len(playlist) >= maxlen:
                    raise HTTPError(409, 'Queue full')
                client.add(file)

            client.play()

    def delete(self, position: int):
        """
        Remove a track from the queue.

        The queue position of the track to be removed is expected to be passed
        in the URL.

        Removing tracks from the queue can be allowed / disallowed using the
        'enable_song_removal' configuration option.

        Parameters
        ----------
        position : int
            position in the queue to remove

        Returns
        -------
        This method does not return anything.

        Exceptions
        ----------
        - If removing items from the queue has been disabled, a HTTP 403 error
          is raised.
        - If the supplied position is not valid, a HTTP 400 error is raised.
        """
        if not self._cfg.get('enable_song_removal'):
            raise HTTPError(403)

        with self._mpd as client:
            try:
                client.delete(position)
            except CommandError as exc:
                raise HTTPError(400, str(exc)) from exc


class StatusHandler(RequestHandler):
    # pylint: disable=abstract-method
    """
    A RequestHandler that returns the current MPD status.

    Methods
    -------
    get():
        Get the current status
    """
    def initialize(self, mpd: MPDContext):
        # pylint: disable=attribute-defined-outside-init
        """Initialize the StatusHandler object"""
        self._mpd = mpd

    def get(self):
        """
        Returns the current MPD status.

        This includes the currently playing song as well as the length of the
        queue.
        """
        with self._mpd as client:
            status = client.status()
            status.update(client.currentsong())
            status.update({'queueLength': len(client.playlist())})

        if 'pos' in status:
            status['queueLength'] -= int(status['pos'])+1

        self.write(status)
