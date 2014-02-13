# Sublime Open

Open files easier and faster in Sublime Text.
Includes a dynamic browser and a static list of files.

## Usage

Open the command palette (on the mac `CMD+SHIFT+P`) and type `Open` should see the 2 options below

### Browser

Browse the directories (starting dir is configurable) until a file is chosen and open that file.
Chosing a directory will list that directory files.

Default: Home dir (`~`)

**Why**

I like to keep all my code under `~/code` but sometimes while I work on a project I need to open a
file from other project or a open a file I just downloaded (`~/Downloads`).

With this is not necessary to open Finder and look for the files.

### Static files

Lists a predefined list of files. Supports wilcards (see settings below).

Default: empty

**Why?**

To manage multiple remote intances in the cloud (EC2) I use the ssh config file under `~/.ssh/config`
I often have to modify this file a few times a day.

The easier solution is to add the `.ssh` directory in the project but I have multiple sublime projects
and I like to keep only the necessary files per project.

## Settings

Under `Preferences > Package Settings > Open > Settings - User``

```
{
    "static_files": ["~/.ssh/config"]   OR   ["~/.ssh/*"],
    "browser_starting_dirs": ["~/code", "~/Downloads"],
    "filter_files": ["\\.DS_Store", "\\.git"],
}

```


