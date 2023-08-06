"""
Test the auto-queue functionality

If enabled, auto-queue should feed the jukebox with new songs to play if the
queue runs empty. It can optionally be fine-tuned by specifying a genre or a
playlist from which to choose the songs.
"""
from unittest.mock import MagicMock
from fookebox.autoqueue import AutoQueuer
from tests.common import MockMPD


class AutoQueueTest:
    """This is a superclass for all tests in thie file"""
    # pylint: disable=too-few-public-methods
    def setup_method(self):
        """The MockMPD and AutoQueuer are used in most tests below"""
        # pylint: disable=attribute-defined-outside-init
        self.mpd = MockMPD()
        self.queuer = AutoQueuer(self.mpd, 5)


class TestAutoQueue(AutoQueueTest):
    """
    Test the auto-queue mechanism.

    The auto-queuer should check the current state to figure out whether a new
    song should be added to the queue.
    """
    def test_requires_no_new_file_when_playing(self):
        """Do not require a new file if there is enough time left"""
        status = {
            'duration': '138.669',
            'elapsed': '48.446'
        }

        # pylint: disable=protected-access
        assert not self.queuer._requires_new_file(status)

    def test_requires_no_new_file_when_another_song_is_queued(self):
        """Do not require a new file if there is something else in the queue"""
        status = {
            'duration': '138.669',
            'elapsed': '138.400',
            'nextsong': '1'
        }

        # pylint: disable=protected-access
        assert not self.queuer._requires_new_file(status)

    def test_requires_new_file_when_playing_is_almost_over(self):
        """Require a new file if the current song is almost over"""
        status = {
            'duration': '138.669',
            'elapsed': '135'
        }

        # pylint: disable=protected-access
        assert self.queuer._requires_new_file(status)


class TestAutoQueuePlaylist(AutoQueueTest):
    """
    Test the auto-queue-playlist functionality.

    If a playlist has been specified, auto-queue should pick the next unplayed
    song from that playlist.
    """
    def setup_method(self):
        super().setup_method()
        self.mpd.mpd_playlists["test"] = ["01", "02", "03"]

    def test_auto_queue_playlist_issues_play_command(self):
        """Auto-queue from a playlist should issue a 'play' command"""
        assert len(self.mpd.commands) == 0

        queuer = AutoQueuer(self.mpd, 5, playlist='test101')
        queuer.auto_queue()
        assert len(self.mpd.commands) == 1
        assert self.mpd.commands[0] == 'play'

        queuer.auto_queue()
        assert len(self.mpd.commands) == 2
        assert self.mpd.commands[0] == 'play'
        assert self.mpd.commands[1] == 'play'

    def test_auto_queue_use_playlist_when_configured(self):
        """
        If a playlist has been configured, auto-queue should only play songs
        from that playlist.
        """
        # pylint: disable=protected-access
        queuer = AutoQueuer(self.mpd, 5)
        queuer._auto_queue_playlist = MagicMock()
        queuer.auto_queue()
        queuer._auto_queue_playlist.assert_not_called()

        queuer = AutoQueuer(self.mpd, 5, playlist='test101')
        queuer._auto_queue_playlist = MagicMock()
        queuer.auto_queue()
        queuer._auto_queue_playlist.assert_called()

    def test_auto_queue_from_playlist_rotate(self):
        """Start from scratch once the playlist has been fully played"""
        assert len(self.mpd.mpd_queue) == 0

        queuer = AutoQueuer(self.mpd, 5, playlist='test')
        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 1
        assert self.mpd.mpd_queue[0] == "01"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 2
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 3
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"
        assert self.mpd.mpd_queue[2] == "03"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 4
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"
        assert self.mpd.mpd_queue[2] == "03"
        assert self.mpd.mpd_queue[3] == "01"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 5
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"
        assert self.mpd.mpd_queue[2] == "03"
        assert self.mpd.mpd_queue[3] == "01"
        assert self.mpd.mpd_queue[4] == "02"

    def test_auto_queue_from_playlist_that_changes(self):
        """Restart from the top if our playlist gets shorter"""
        assert len(self.mpd.mpd_queue) == 0

        queuer = AutoQueuer(self.mpd, 5, playlist='test')
        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 1
        assert self.mpd.mpd_queue[0] == "01"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 2
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"

        self.mpd.mpd_playlists["test"] = ["01"]

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 3
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"
        assert self.mpd.mpd_queue[2] == "01"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 4
        assert self.mpd.mpd_queue[0] == "01"
        assert self.mpd.mpd_queue[1] == "02"
        assert self.mpd.mpd_queue[2] == "01"
        assert self.mpd.mpd_queue[3] == "01"

    def test_auto_queue_from_empty_playlist(self):
        """Auto-queue from empty playlist: Quietly do nothing"""
        assert len(self.mpd.mpd_queue) == 0

        queuer = AutoQueuer(self.mpd, 5, playlist='test1')
        self.mpd.mpd_playlists["test1"] = []
        queuer.playlist = "test1"

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0


class TestAutoQueueGenre(AutoQueueTest):
    """
    Test the auto-queue-genre functionality.

    If a genre has been specified, auto-queue should pick any random song from
    the specified genre from mpd and start playing it.
    """
    def test_auto_queue_use_genre_when_configured(self):
        """
        If a genre has been configured, auto-queue should only play songs from
        that genre.
        """
        # pylint: disable=protected-access
        queuer = AutoQueuer(self.mpd, 5)
        queuer._auto_queue_genre = MagicMock()
        queuer.auto_queue()
        queuer._auto_queue_genre.assert_not_called()

        queuer = AutoQueuer(self.mpd, 5, genre='House')
        queuer._auto_queue_genre = MagicMock()
        queuer.auto_queue()
        queuer._auto_queue_genre.assert_called()

    def test_auto_queue_genre_issue_play_command(self):
        """Auto-queue with a genre should issue a 'play' command"""
        assert len(self.mpd.commands) == 0

        queuer = AutoQueuer(self.mpd, 5, genre='House')
        queuer.auto_queue()

        assert len(self.mpd.commands) == 1
        assert self.mpd.commands[0] == "play"

    def test_auto_queue_from_genre(self):
        """Auto queue any random file from a specific genre"""
        self.mpd.mpd_files.append({"file": "J1", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J2", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J3", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J4", "genre": "Blues"})

        assert len(self.mpd.mpd_queue) == 0

        queuer = AutoQueuer(self.mpd, 5, genre='Jazz')

        for i in range(20):
            # pylint: disable=protected-access
            queuer._auto_queue_genre(self.mpd)
            assert self.mpd.mpd_queue[i] in ["J1", "J2", "J3"]

    def test_auto_queue_from_genre_with_single_file(self):
        """Auto-queue if only 1 file from genre: Always play the same file"""
        self.mpd.mpd_files.append({"file": "J1", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J2", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J3", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J4", "genre": "Blues"})

        assert len(self.mpd.mpd_queue) == 0

        queuer = AutoQueuer(self.mpd, 5, genre='Blues')
        queuer.auto_queue()
        queuer.auto_queue()
        queuer.auto_queue()

        assert len(self.mpd.mpd_queue) == 3
        assert self.mpd.mpd_queue[0] == "J4"
        assert self.mpd.mpd_queue[1] == "J4"
        assert self.mpd.mpd_queue[2] == "J4"

    def test_auto_queue_from_genre_with_no_files(self):
        """Auto-queue if there are no files in genre: Quietly do nothing"""
        self.mpd.mpd_files.append({"file": "J1", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J2", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J3", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J4", "genre": "Blues"})

        assert len(self.mpd.mpd_queue) == 0
        queuer = AutoQueuer(self.mpd, 5, genre='Electro')

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0

        queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0


class TestAutoQueueAny(AutoQueueTest):
    """
    Test the generic auto-queue functionality.

    If no genre or playlist have been specified, auto-queue should pick any
    random song from mpd and start playing it.
    """
    def test_auto_queue_any_issues_play_command(self):
        """Auto-queue should issue a 'play' command"""
        assert len(self.mpd.commands) == 0

        self.queuer.auto_queue()

        assert len(self.mpd.commands) == 1
        assert self.mpd.commands[0] == "play"

    def test_auto_queue_queues_any_if_not_otherwise_configured(self):
        """By default, auto-queue should pick any random song from mpd"""
        # pylint: disable=protected-access
        self.queuer._auto_queue_any = MagicMock()

        self.queuer.auto_queue()
        assert self.queuer._auto_queue_any.call_count == 1

        self.queuer.auto_queue()
        assert self.queuer._auto_queue_any.call_count == 2

    def test_auto_queue_does_not_use_autoqueue_any_if_genre_is_set(self):
        """
        If a genre has been configured, auto-queue should only play songs from
        that genre.
        """
        # pylint: disable=protected-access
        queuer = AutoQueuer(self.mpd, 5, genre='Electro')
        queuer._auto_queue_any = MagicMock()
        queuer.auto_queue()
        queuer._auto_queue_any.assert_not_called()

        queuer = AutoQueuer(self.mpd, 5)
        queuer._auto_queue_any = MagicMock()
        queuer.auto_queue()
        queuer._auto_queue_any.assert_called_once()

    def test_auto_queue_any(self):
        """Auto queue any random file"""
        self.mpd.mpd_files.append({"file": "334"})
        self.mpd.mpd_files.append({"file": "335"})
        self.mpd.mpd_files.append({"file": "336"})

        assert len(self.mpd.mpd_queue) == 0

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 1
        assert self.mpd.mpd_queue[0] in ['334', '335', '336']

        for _ in range(20):
            self.queuer.auto_queue()

        assert len(self.mpd.mpd_queue) == 21

    def test_auto_queue_do_not_play_directory(self):
        """Auto queue any random file: Do *not* try to play a directory"""
        self.mpd.mpd_files.append({"directory": "334"})
        self.mpd.mpd_files.append({"directory": "335"})
        self.mpd.mpd_files.append({"directory": "336"})

        assert len(self.mpd.mpd_queue) == 0

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0

    def test_auto_queue_any_does_not_repeat_the_same_song(self):
        """Auto-queue should not ever play the same file twice in a row"""
        files = [{'file': str(i)} for i in range(15)]
        self.mpd.mpd_files = files

        for i in range(200):
            self.queuer.auto_queue()

        for i in range(199):
            assert self.mpd.mpd_queue[i] != self.mpd.mpd_queue[i+1]

    def test_auto_queue_any_single_song(self):
        """Auto-queue if only 1 file available: Always play the same file"""
        self.mpd.mpd_files.append({'file': '354'})

        assert len(self.mpd.mpd_queue) == 0

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 1
        assert self.mpd.mpd_queue[0] == '354'

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 2
        assert self.mpd.mpd_queue[0] == '354'
        assert self.mpd.mpd_queue[1] == '354'

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 3
        assert self.mpd.mpd_queue[0] == '354'
        assert self.mpd.mpd_queue[1] == '354'
        assert self.mpd.mpd_queue[2] == '354'

    def test_auto_queue_any_no_songs(self):
        """Auto-queue if there are no files available: Quietly do nothing"""
        self.mpd.mpd_files = []

        assert len(self.mpd.mpd_queue) == 0

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0

        self.queuer.auto_queue()
        assert len(self.mpd.mpd_queue) == 0
