from os.path import dirname, isdir

from sublime import ENCODED_POSITION, set_timeout
from sublime_plugin import TextCommand

from .Files import Bookmarks, DirListing
from .Settings import SettingsProxy
from .Tools import Future

class OpenBrowseCommand(TextCommand, SettingsProxy):

    def working_dir(self):
        return self.view.file_name() and dirname(self.view.file_name())

    def run(self, cmd):
        self.quick_panel = QuickPanelTask(self.view.window())
        self.bind_settings(('persistent_browsing', 'list_active_folder'))
        self.list_bookmarks()

    def list_bookmarks(self):
        files = Bookmarks()
        if self._list_active_folder and self.working_dir():
            files += DirListing(self.working_dir())
        self.show_quick_panel(files)

    def show_quick_panel(self, files):
        self.quick_panel.show(files.labels(), files).then(self.open)

    def open(self, entry):
        if isdir(entry.path):
            return self.list_dir(entry.path)
        self.open_file(entry.path)
        if self._persistent_browsing:
            self.open(entry._replace(path=dirname(entry.path)))

    def list_dir(self, path):
        self.show_quick_panel(DirListing(path))

    def open_file(self, path):
        self.view.window().open_file(path, ENCODED_POSITION)

class QuickPanelTask:

    def __init__(self, window):
        self.__window = window

    def show(self, items, values=None):
        def show(resolve, reject):
            # XXX: https://github.com/danielfrg/sublime-open/issues/1
            set_timeout(lambda: self.__window.show_quick_panel(items,
                lambda i: reject() if i is -1 else resolve((values or items)[i])), 0)
        return Future(show)
