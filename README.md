# Sublime Open

Open files easier and faster in Sublime Text using bookmarks or a file browser.

## Usage

Default hotkey is `CMD+SHIFT+o`

A panel will appear with the defined bookmarks, files and directories:

 * Files will be opened in a new tab
 * Directories can be navigated inside sublime

## Settings

`Preferences > Package Settings > Open > Settings - User`

Example:

```
{
    // Files or directories to be shown at the begining
    "bookmarks": ["~", "~/.ssh/config"],

    // Bookmark identifier in the first panel. Can be "%d" to enumerate them
    "bookmark_prefix": "»",

    // List the directory of the currently file (tab)
    "list_current_dir": true,

    // Ignore regex patters
    "filter_regex": ["\\.DS_Store", "\\.git"]
}
```

Bookmarks will the the home directory of the user and a static ssh config file.

Since `list_current_dir` is true it will show first the bookmarks (prefixed
by the `»`) symbol and then will list the files and directories of the current opened
file (current tab).

It will ignore the `.DS_Store` files and `.git` directories.
