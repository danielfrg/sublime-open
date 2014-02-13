import sublime
import sublime_plugin

import os
import re
import glob


SETTINGS_FILE = 'Open.sublime-settings'
settings = sublime.load_settings(SETTINGS_FILE)
static_files = []


def reload_static_files():
    global static_files
    static_files = []
    for pattern in settings.get('static_files', list()):
        if os.path.isdir(pattern):
            static_files.append(pattern)
        else:
            pattern = os.path.expanduser(pattern)
            matching = glob.glob(pattern)
            static_files.extend(matching)


def filter_files(fname):
    """
    Returns False if a file should be ignored: If the file matched any of the regular expressions
    on the settings file
    """
    fname = os.path.basename(fname)
    filters = settings.get('default_filter_files', list())
    filters.extend(settings.get('filter_files', list()))
    for regex in filters:
        regex = regex.replace('\\\\', '\\')  # Fix backslash scaping on json
        p = re.compile(regex)
        if p.match(fname) is not None:
            return False
    return True


reload_static_files()


class OpenCommand(sublime_plugin.TextCommand):

    def show_panel(self):
        self.items.append('-')
        func = lambda: self.view.window().show_quick_panel(self.items, self.open_by_idx)
        sublime.set_timeout(func, 10)

    def open_by_idx(self, index):
        if self.items[index] == '-':
            # Using escape to cancel is always opening the last item in the list
            return None
        fname = self.items[index]
        self.open(fname)

    def open(self, fname):
        """
        If fname is a directory will list the files and directories
        If fname is a file will open that file
        """
        if os.path.isdir(fname):
            self.currentdir = fname
            self.items = [os.path.join(fname, t) for t in os.listdir(fname) if filter_files(t)]
            self.show_panel()
        else:
            self.view.window().open_file(fname, sublime.ENCODED_POSITION)


class OpenStaticCommand(OpenCommand):

    def run(self, edit):
        self.items = static_files
        self.items = [os.path.abspath(t) for t in self.items if filter_files(t)]
        self.show_panel()


class OpenBrowser(OpenCommand):

    def show_panel(self):
        if self.currentdir is not None:
            # self.currentdir is None on the first screen
            self.items = ['..'] + self.items
        super(OpenBrowser, self).show_panel()

    def open_by_idx(self, index):
        if self.items[index] == '..':
            # Go to the parent dir
            fname = os.path.abspath(os.path.join(self.currentdir, os.pardir))
            self.open(fname)
        else:
            super(OpenBrowser, self).open_by_idx(index)

    def run(self, edit):
        self.currentdir = None
        self.items = settings.get('browser_starting_dirs', list())
        self.items = [os.path.expanduser(f) for f in self.items]
        self.items = [os.path.abspath(f) for f in self.items]
        self.items = [f for f in self.items if filter_files(f)]
        self.show_panel()


class ReloadStaticFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        reload_static_files()
