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
This is our interface to the python-mpd2 library. It consists of one single
class, which serves as a context manager and connects to MPD.
"""

from mpd import MPDClient


class MPDContext:
    """
    The MPDContext class is a context manager that connects to MPD. It can be
    used like this:

      mpd = MPDContext('localhost', 6600)
      with mpd as client:
          print(client.status())

    """
    def __init__(self, host: str, port: int, password: str = ''):
        """
        Constructs all the necessary attributes for the MPDContext object

        Parameters
        ----------
        host : str
            MPD host to connect to
        port : int
            MPD port to connect to
        password : str, optional
            MPD passwort, if required
        """
        self._host = host
        self._port = port
        self._password = password
        self._client = MPDClient()

    def __enter__(self):
        self._client.connect(self._host, self._port)
        self._client.consume(1)

        if self._password:
            self._client.password(self._password)

        return self._client

    def __exit__(self, *args):
        self._client.disconnect()
