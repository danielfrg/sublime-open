from sublime import load_settings

class SettingsProxy:
    keys = [
	    'bookmarks',
	    'bookmark_prefix',
	    'persistent_browsing',
	    'list_working_dir',
	    'list_dirs_first',
    ]
    app_keys = ['folder_exclude_patterns', 'file_exclude_patterns']

    def __init__(self):
        for key in self.keys + self.app_keys:
            setattr(self, key, load_settings('Open.sublime-settings').get(key))
        for key in self.app_keys:
            if getattr(self, key) is None:
                setattr(self, key, load_settings('Preferences.sublime-settings').get(key))
