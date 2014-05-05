import sublime
import sublime_plugin

import os
import re


class OpenBrowseCommand(sublime_plugin.TextCommand):

    settings_file = 'Open.sublime-settings'

    def show_panel(self):
        if self.currentdir is not None:
            # self.currentdir is None on the first screen, don't show parent dir option
            self.display.insert(0, '..')
            self.items.insert(0, os.path.abspath(os.path.join(self.currentdir, os.pardir)))

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
            if os.path.isdir(fname):
                self.currentdir = fname
                self.display = [f for f in os.listdir(fname) if self.filter_files(f)]
                self.items = [os.path.join(fname, f) for f in self.display]
                self.show_panel()
            elif os.path.exists(fname):
                sublime.set_timeout(lambda: self.view.window().open_file(fname, sublime.ENCODED_POSITION), 0)

    def run(self, cmd):
        self.settings = sublime.load_settings(self.settings_file)

        self.currentdir = None
        self.display = []
        self.items = []

        # List the bookmarks
        self.display = self.settings.get('bookmarks', list())
        self.items = [os.path.expanduser(f) for f in self.display]
        self.items = [os.path.abspath(f) for f in self.items]
        self.items = [f for f in self.items if self.filter_files(f)]

        self.show_panel()

    def filter_files(self, fname):
        """
        Returns False if a file should be ignored: If the file matched any of the regular expressions
        on the settings file
        """
        fname = os.path.basename(fname)
        for regex in self.settings.get('filter_regex', list()):
            regex = regex.replace('\\\\', '\\')  # Fix backslash scaping on json
            p = re.compile(regex)
            if p.match(fname) is not None:
                return False
        return True
