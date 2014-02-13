# Sublime Open

Open files easier and faster in Sublime Text.
Includes a dynamic browser and a static list of files (bookmarks).

## Usage

Default hotkey is `CMD+SHIFT+o` or using the command palette (`CMD+SHIFT+p`)

A panel will appear with the defined bookmarks, files and directories:

 * Files will be opened in a new tab
 * Directories you can navigate them in sublime

## Settings

Under `Preferences > Package Settings > Open > Settings - User``

Bookmarks below will be you home directory and a static file of the ssh config.

```
{
    // Files or directories to be shown at the begining
    "bookmarks": ["~", "~/.ssh/config"],

    // Ignore regex patters
    "filter_regex": ["\\.DS_Store"]
}
```