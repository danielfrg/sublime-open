from fnmatch import fnmatch
from os import listdir, pardir
from os.path import abspath, basename, dirname, expanduser, isdir, join

class FilesList:

    def __init__(self, settings):
        self.settings = settings

        self.bookmark_format = self.settings.bookmark_prefix
        for sub in [('{', '{{'), ('}', '}}'), ('#', '{1}')]:
            self.bookmark_format = self.bookmark_format.replace(sub[0], sub[1])
        self.bookmark_format = self.bookmark_format + ' {0}'

        self.paths = []
        self.labels = []

    def add_dir_contents(self, path):
        if not path:
            return
        if not isdir(path):
            path = dirname(path)

        self.__add_dir_decorators(path)
        format_dir_contents = lambda f, i: join(basename(f), '') if isdir(f) else basename(f)
        self.add_files(self.__glob(path), format_dir_contents)

    def add_bookmarks(self):
        self.add_files(self.settings.bookmarks, self.bookmark_format.format)

    def add_files(self, paths, labels_or_format_fn):
        self.paths += [abspath(expanduser(f)) for f in paths]
        if callable(labels_or_format_fn):
            labels_or_format_fn = [labels_or_format_fn(f, i) for i, f in enumerate(paths)]
        self.labels += labels_or_format_fn

    def __add_dir_decorators(self, basedir):
        self.add_files([join(basedir, pardir)], ['..'])

    def __glob(self, basedir):
        paths = [join(basedir, f) for f in listdir(basedir) if self.__fnmatch(basedir, f)]
        return self.__sort(paths) if self.settings.list_dirs_first else paths

    def __fnmatch(self, basedir, fname):
        patterns = self.settings.folder_exclude_patterns if isdir(join(basedir, fname)) \
            else self.settings.file_exclude_patterns
        return not any([fnmatch(fname, p) for p in patterns])

    def __sort(self, paths):
        dirs = [f for f in paths if isdir(f)]
        return dirs + [f for f in paths if not f in dirs]
