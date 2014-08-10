from collections import namedtuple

from sublime import load_settings

from .Tools import lazy

class SettingsProxy:
    __Chain = namedtuple('__Chain', 'plugin app')

    def bind_settings(self, plugin=(), app=()):
        for setting in plugin:
            setattr(self, '_{}'.format(setting), self._settings.plugin.get(setting))
        for setting in app:
            value = self._settings.plugin.get(setting, self._settings.app.get(setting))
            setattr(self, '_{}'.format(setting), value)

    @lazy
    def _settings(self):
        return self.__Chain(
            plugin=load_settings('Open.sublime-settings'),
            app=load_settings('Preferences.sublime-settings'))
