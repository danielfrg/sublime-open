from os.path import curdir, dirname, isdir

from sublime import ENCODED_POSITION, TRANSIENT, set_timeout
from sublime_plugin import TextCommand

from .Files import Bookmarks, DirListing
from .Settings import SettingsProxy
from .Tools import Future, unexpanduser

class OpenBrowseCommand(TextCommand, SettingsProxy):

    def working_dir(self):
        return self.view.file_name() and dirname(self.view.file_name())

    def run(self, cmd):
        self.quick_panel = QuickPanelTask(self.view.window())
        self.bind_settings(
            plugin=('persistent_browsing', 'list_active_folder'),
            app=('preview_on_click',))
        self.list_bookmarks()

    def list_bookmarks(self):
        files = Bookmarks()
        if self.working_dir():
            if self._list_active_folder:
                files += DirListing(self.working_dir())
            else:
                # FIXME: prevent duplicate bookmark
                files = Bookmarks((unexpanduser(self.working_dir()),), 0) + files
        self.show_quick_panel(files)

    def show_quick_panel(self, files):
        self.quick_panel.show(files.labels(), files).then(self.open)

    def open(self, entry):
        if entry.name is curdir:
            return self.open_dir(entry.path)
        if isdir(entry.path):
            return self.list_dir(entry.path)
        self.open_file(entry.path)
        if self._persistent_browsing:
            self.open(entry._replace(path=dirname(entry.path)))

    def list_dir(self, path):
        self.show_quick_panel(DirListing(path))

    def open_dir(self, path):
        project = self.view.window().project_data() or {}
        project.setdefault('folders', [])
        if path in [x['path'] for x in project['folders']]:
            return
        folder = {'path': path, 'follow_symlinks': True}
        folder.update({s: self._settings.plugin.get(s) for s in DirListing._filter_settings \
            if self._settings.plugin.has(s)})
        project['folders'] += [folder]
        self.view.window().set_project_data(project)

    def open_file(self, path):
        flags = ENCODED_POSITION | TRANSIENT if self._preview_on_click else ENCODED_POSITION
        self.view.window().open_file(path, flags)

class QuickPanelTask:

    def __init__(self, window):
        self.__window = window

    def show(self, items, values=None):
        def show(resolve, reject):
            # XXX: https://github.com/danielfrg/sublime-open/issues/1
            set_timeout(lambda: self.__window.show_quick_panel(items,
                lambda i: reject() if i is -1 else resolve((values or items)[i])), 0)
        return Future(show)

# TODO: class InputPanelTask:
