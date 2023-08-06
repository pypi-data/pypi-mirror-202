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
This is the main file for fookebox. It provides the 'main()' entry point as
well as a bunch of helper functions.
"""

import asyncio
import os.path
import sys

from argparse import ArgumentParser
from configparser import SectionProxy
from importlib import resources

from tornado import locale
from tornado.web import Application

import fookebox
from .autoqueue import AutoQueuer
from .config import load_config, default_config
from .mpd import MPDContext
from .handlers import ArtistHandler, ControlHandler, CoverArtHandler
from .handlers import CSSHandler, FontHandler, GenreHandler, IndexHandler
from .handlers import JSHandler, QueueHandler, StatusHandler


def _make_app(config, mpd: MPDContext):
    res = resources.files(fookebox).joinpath('i18n')
    with resources.as_file(res) as dir_:
        locale.load_gettext_translations(str(dir_), domain='fookebox')
    locale.set_default_locale('en')

    return Application([
        (r'/', IndexHandler,
            {'mpd': mpd, 'cfg': config}),
        (r'/status', StatusHandler,
            {'mpd': mpd}),
        (r'/css/(.*)', CSSHandler),
        (r'/js/(.*)', JSHandler),
        (r'/fonts/(.*)', FontHandler),
        (r'/artist/(.*)', ArtistHandler,
            {'mpd': mpd}),
        (r'/genre/(.*)', GenreHandler,
            {'mpd': mpd}),
        (r'/queue/(\d+)', QueueHandler,
            {'mpd': mpd, 'cfg': config}),
        (r'/queue', QueueHandler,
            {'mpd': mpd, 'cfg': config}),
        (r'/control', ControlHandler,
            {'mpd': mpd, 'cfg': config}),
        (r'/cover/(.*)', CoverArtHandler,
            {'mpd': mpd, 'cfg': config}),
    ])


def _parse_args():
    parser = ArgumentParser(description='Jukebox server')
    parser.add_argument('-c', '--config', required=False,
                        help='configuration file')
    parser.add_argument('--version', action='version',
                        version=f'fookebox { fookebox.__version__ }',
                        help='show version information')
    return parser.parse_args()


async def _auto_queue(mpd, config: SectionProxy):
    auto_queue_at = config.getint('auto_queue_time_left')
    queuer = AutoQueuer(mpd, auto_queue_at)

    while True:
        try:
            queuer.auto_queue()
        except ConnectionRefusedError as exc:
            print(exc)
        await asyncio.sleep(1)


async def main():
    """
    This is the main function. It parses the command line arguments, loads the
    config file and starts the application.
    """
    args = _parse_args()

    if args.config:
        if not os.path.exists(args.config):
            print(f'{args.config} not found', file=sys.stderr)
            sys.exit(1)
        cfg = load_config(args.config)
    else:
        cfg = default_config()

    mpd = MPDContext(cfg.get('mpd_host'), cfg.get('mpd_port'))

    if cfg.getboolean('auto_queue'):
        asyncio.create_task(_auto_queue(mpd, cfg))

    app = _make_app(cfg, mpd)
    port = cfg.getint('listen_port')
    print(f'Listening on http://localhost:{port}/')
    app.listen(port)
    await asyncio.Event().wait()


if __name__ == 'fookebox.fookebox':
    asyncio.run(main())
