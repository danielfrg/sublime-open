import sublime
import sublime_plugin

import re
import os
from os.path import join, dirname, abspath, isdir, basename, expanduser, exists


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
                self.display = []
                self.items = []
                self.list_files(fname)
                self.show_panel()
            elif exists(fname):
                sublime.set_timeout(lambda: self.view.window().open_file(fname, sublime.ENCODED_POSITION), 0)

    def run(self, cmd):
        self.settings = sublime.load_settings(self.settings_file)

        self.display = []
        self.items = []

        # List bookmarks
        self.list_bookmarks()

        # List current file (tab) directory
        fname = self.view.window().active_view().file_name()
        if self.settings.get('list_current_dir', True) and fname is not None:
            self.list_files(dirname(fname))

        self.show_panel()

    def list_bookmarks(self):
        bookmarks = self.settings.get('bookmarks', list())

        bookmark_icon = self.settings.get('bookmark_prefix', '»')
        if bookmark_icon == '%d':
            self.display += ['%d: %s ' % (i, f) for i, f in enumerate(bookmarks)]
        else:
            self.display += [bookmark_icon + ' ' + f for f in bookmarks]

        bookmarks = [abspath(expanduser(f)) for f in bookmarks]
        self.items += [f for f in bookmarks]

    def list_files(self, fname):
        self.currentdir = fname

        # Parent dir
        self.display += ['..']
        self.items +=  [abspath(join(self.currentdir, os.pardir))]

        # List files and dirs
        self.display += [join(f, '') if isdir(join(fname, f)) else f for f in os.listdir(fname) if self.filter_files(f)]
        self.items += [join(fname, f) for f in os.listdir(fname) if self.filter_files(f)]

    def filter_files(self, fname):
        """
        Returns False if a file should be ignored: If the file matched any of the regular expressions
        on the settings file
        """
        fname = basename(fname)
        for regex in self.settings.get('filter_regex', list()):
            regex = regex.replace('\\\\', '\\')  # Fix backslash escaping on json
            p = re.compile(regex)
            if p.match(fname) is not None:
                return False
        return True
