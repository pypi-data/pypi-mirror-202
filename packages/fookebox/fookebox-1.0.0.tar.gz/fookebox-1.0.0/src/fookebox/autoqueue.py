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
The AutoQueuer is an optional feature that automatically picks songs to play
if the queue runs empty.
"""

import random
from mpd import MPDClient
from .mpd import MPDContext


class AutoQueuer:
    """
    A class to automatically pick songs to play if the queue runs empty.

    Methods
    -------
    auto_queue():
        Checks whether a new songs needs to be added to the queue and, if so,
        picks one, adds it and issues a 'play' command.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, mpd: MPDContext, auto_queue_at: int, *,
                 genre: str = '', playlist: str = ''):
        """
        Constructs all the necessary attributes for the AutoQueuer object

        Parameters
        ----------
        mpd : MPDContext
            MPDContext instance to use to connect to MPD
        auto_queue_at : int
            if the remaining time falls below this value, we add a new song
        genre : str, optional
            if this is set, limit automatically picked songs to this genre
        playlist: str, optional
            if this is set, pick the next song from this playlist
        """
        self._mpd = mpd
        self._auto_queue_at = auto_queue_at
        self._genre = genre
        self._playlist = playlist
        self._history: list[str] = []
        self._playlist_offset = 0

    def _requires_new_file(self, status: dict[str, str]):
        duration = float(status.get('duration', 0))
        elapsed = float(status.get('elapsed', 0))
        nextsong = status.get('nextsong')
        timeleft = duration - elapsed

        return timeleft <= self._auto_queue_at and nextsong is None

    def _auto_queue_random(self, client: MPDClient,
                           entries: list[dict[str, str]]):
        files = [row['file'] for row in entries if 'file' in row]
        valid = [file for file in files if file not in self._history]

        # if no valid files are left, consider *all* files valid
        if len(valid) < 1:
            valid = files

        if len(valid) > 0:
            file = random.choice(valid)

            self._history.append(file)
            while len(self._history) > len(valid) / 10:
                del self._history[0]

            client.add(file)

    def _auto_queue_any(self, client: MPDClient):
        entries = client.listall()
        self._auto_queue_random(client, entries)

    def _auto_queue_genre(self, client: MPDClient):
        entries = client.find('genre', self._genre)
        self._auto_queue_random(client, entries)

    def _auto_queue_playlist(self, client: MPDClient):
        entries = client.listplaylist(self._playlist)

        # the playlist has shrunk, start from scratch
        if len(entries) <= self._playlist_offset:
            self._playlist_offset = 0

        if len(entries) > self._playlist_offset:
            client.add(entries[self._playlist_offset])
            self._playlist_offset = (self._playlist_offset + 1) % len(entries)

    def auto_queue(self):
        """
        Automatically select a song to be added to the queue.

        - If we are configured to play a specific genre, pick a song from
          that genre.
        - If we are configured to choose from a particular playlist, pick the
          next unplayed song from that playlist.
        - Otherwise, pick a random song from the MPD library that has not been
          played for a while.
        """
        with self._mpd as client:
            status = client.status()
            if self._requires_new_file(status):
                if self._genre:
                    self._auto_queue_genre(client)
                elif self._playlist:
                    self._auto_queue_playlist(client)
                else:
                    self._auto_queue_any(client)
                client.play()
