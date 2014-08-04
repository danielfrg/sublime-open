from os.path import isdir

from sublime import ENCODED_POSITION, set_timeout
from sublime_plugin import TextCommand

from .Files import FilesList
from .Settings import SettingsProxy

class OpenBrowseCommand(TextCommand):

    def run(self, cmd):
        self.settings = SettingsProxy()
        self.files = FilesList(self.settings)

        self.files.add_bookmarks()
        if self.settings.list_working_dir:
            self.files.add_dir_contents(self.view.window().active_view().file_name())

        self.show_panel()

    def show_panel(self):
        show_panel = lambda: self.view.window().show_quick_panel(self.files.labels, self.open)
        # XXX: https://github.com/danielfrg/sublime-open/issues/1
        set_timeout(show_panel, 0)

    def open(self, index):
        if index is -1:
            return
        path = self.files.paths[index]

        if isdir(path):
            self.list_dir(path)
        else:
            self.open_file(path)
            if self.settings.persistent_browsing:
                self.show_panel()

    def list_dir(self, path):
        self.files = FilesList(self.settings)
        self.files.add_dir_contents(path)
        self.show_panel()

    def open_file(self, path):
        open_file = lambda: self.view.window().open_file(path, ENCODED_POSITION)
        # XXX: Why?
        set_timeout(open_file, 0)
