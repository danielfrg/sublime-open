from collections import namedtuple
from itertools import starmap
from os.path import abspath, expanduser, join

from .Tools import lazy

# inspired by: algebraic data types
class _FilesList:
    __Entry = namedtuple('__Entry', 'name path label')

    def __init__(self, names, base_dir=None):
        self._names = names
        if base_dir:
            self._base_dir = base_dir
        # delegate to type(self).mro() e.g. SettingsProxy
        super().__init__()

    def labels(self):
        return [e.label for e in self._entries]

    @lazy
    def _entries(self):
        # build and associate paths with names
        entries = zip(self._names, map(self._normalize_path, self._names))
        delattr(self, '_names')
        # filter by paths
        entries = filter(lambda x: self._filter_path(*x), entries)
        # associate indexes for labels
        entries = [self.__Entry(k, p, i) for i, (k, p) in enumerate(entries)]
        # build and associate labels
        entries = zip(entries, starmap(self._format_label, entries))
        # replace indexes with labels
        entries = [e._replace(label=l) for e, l in entries]
        # finally sort based on any field
        return sorted(entries, key=lambda e: self._sort_by(*e), reverse=self._reverse_sort())

    def _normalize_path(self, name):
        if hasattr(self, '_base_dir'):
            name = join(self._base_dir, name)
        return abspath(expanduser(name))

    def _filter_path(self, name, path):
        return True

    def _format_label(self, name, path, index):
        return name

    def _sort_by(self, name, path, label):
        # preserve original order
        return 0

    def _reverse_sort(self):
        return False

    def __len__(self):
        return len(self._entries)

    def __contains__(self, path):
        return path in [e.path for e in self._entries]

    def __getitem__(self, index):
        return self._entries[index]

    def __add__(self, other):
        return _FilesCons(self, other)

class _FilesCons(_FilesList):
    __Cons = namedtuple('__Cons', 'head tail')

    def __init__(self, head, tail):
        super().__init__(self.__Cons(head, tail))

    def labels(self):
        return self._names.head.labels() + self._names.tail.labels()

    def __len__(self):
        return len(self._names.head) + len(self._names.tail)

    def __contains__(self, path):
        return path in self._names.head or path in self._names.tail

    def __getitem__(self, index):
        n = len(self._names.head)
        return self._names.head[index] if index < n else self._names.tail[index - n]
