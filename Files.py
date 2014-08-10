from fnmatch import fnmatch
from os import listdir, stat
from os.path import basename, curdir, isdir, join, pardir, sep

from .FilesBase import _FilesCons, _FilesList
from .Settings import SettingsProxy

class Bookmarks(_FilesList, SettingsProxy):

    def __init__(self, paths=None, start_index=1):
        self.__start_index = start_index
        self.bind_settings(('bookmarks', 'bookmark_prefix'))
        self.__label_format = self.__format_prefix(self._bookmark_prefix)
        super().__init__(paths or self._bookmarks)

    def _format_label(self, name, path, index):
        return self.__label_format.format(name, index + self.__start_index)

    def __format_prefix(self, prefix):
        for sub in (('{', '{{'), ('}', '}}'), ('#', '{1}')):
            prefix = prefix.replace(sub[0], sub[1])
        return prefix + ' {0}'

class DirListing(_FilesCons):
    # XXX: only here for access by .Open.OpenBrowseCommand#open_dir()
    _filter_settings = ('folder_exclude_patterns', 'file_exclude_patterns')

    def __init__(self, path):
        super().__init__(_DirDecorators(path), _DirContents(path))

class _DirDecorators(_FilesList):
    __decorators = (curdir, pardir)

    def __init__(self, base_dir):
        super().__init__((curdir,) if base_dir == sep else self.__decorators, base_dir)

    def _format_label(self, name, path, index):
        return '{} [{}]'.format(name, join(basename(path), '') or sep)

class _DirContents(_FilesList, SettingsProxy):

    def __init__(self, base_dir):
        self.bind_settings(
            plugin=('sort_folders_first', 'sort_by_timestamp'),
            app=DirListing._filter_settings)
        super().__init__(listdir(base_dir), base_dir)

    def _filter_path(self, name, path):
        patterns = self._folder_exclude_patterns if isdir(path) else self._file_exclude_patterns
        # map() is lazy in Python 3 for short-circuit evaluation
        return not any(map(lambda p: fnmatch(name, p), patterns))

    def _format_label(self, name, path, index):
        return join(name, '') if isdir(path) else name

    def _sort_by(self, name, path, label):
        key = None
        if self._sort_folders_first:
            # (file, dir) = (1, 0)
            key = int(not isdir(path))
        if self._sort_by_timestamp:
            # separate dirs by 3000 years in nanoseconds
            key = key * 1e20 if key else 0
            status = stat(path)
            # adjust by most recent timestamp
            key -= max(status.st_atime, status.st_mtime, status.st_ctime)
        return super()._sort_by(name, path, label) if key is None else key
