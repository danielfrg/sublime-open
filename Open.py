import sublime
import sublime_plugin

import os
import re

from os.path import *


class OpenBrowseCommand(sublime_plugin.TextCommand):

    settings_file = 'Open.sublime-settings'

    def show_panel(self):
        func = self.open
        elements = self.display
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(elements, func), 10)

    def open(self, index):
        """
        If file is a directory will list the files and directories
        If file is a file will open that file
        """
        if index != -1:
            fname = self.items[index]
            if isdir(fname):
                self.list_files(fname)
                self.show_panel()
            elif exists(fname):
                sublime.set_timeout(lambda: self.view.window().open_file(fname, sublime.ENCODED_POSITION), 0)

    def run(self, cmd):
        self.settings = sublime.load_settings(self.settings_file)

        self.display = []
        self.items = []
        fname = self.view.window().active_view().file_name()
        if fname is not None:
            self.list_files(dirname(fname))
        self.list_bookmarks()
        self.show_panel()

    def list_bookmarks(self):
        bookmarks = self.settings.get('bookmarks', list())
        self.display = ['%d: %s' % (i + 1, f) for i, f in enumerate(bookmarks)] + self.display
        bookmarks = [abspath(expanduser(f)) for f in bookmarks]
        self.items = [f for f in bookmarks if self.filter_files(f)] + self.items

    def list_files(self, fname):
        self.currentdir = fname
        self.display = [join(f, '') if isdir(join(fname, f)) else f for f in os.listdir(fname) if self.filter_files(f)]
        self.items = [join(fname, f) for f in self.display]
        self.display.insert(0, '..')
        self.items.insert(0, abspath(join(self.currentdir, os.pardir)))

    def filter_files(self, fname):
        """
        Returns False if a file should be ignored: If the file matched any of the regular expressions
        on the settings file
        """
        fname = basename(fname)
        for regex in self.settings.get('filter_regex', list()):
            regex = regex.replace('\\\\', '\\')  # Fix backslash scaping on json
            p = re.compile(regex)
            if p.match(fname) is not None:
                return False
        return True
