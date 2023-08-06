[![coBib](https://gitlab.com/mrossinek/cobib/-/raw/master/logo/cobib_logo.svg)](https://mrossinek.gitlab.io/cobib/cobib.html)

# coBib

[![pipeline](https://gitlab.com/mrossinek/cobib/badges/master/pipeline.svg)](https://gitlab.com/mrossinek/cobib/-/pipelines)
[![coverage](https://gitlab.com/mrossinek/cobib/badges/master/coverage.svg)](https://gitlab.com/mrossinek/cobib/-/graphs/master/charts)
[![PyPI](https://img.shields.io/pypi/v/cobib)](https://pypi.org/project/cobib/)

coBib is a simple, command-line based bibliography management tool.
It is the result of the need for an easy-to-use alternative to full-blown reference managers like Mendeley or Zotero.
As such it follows some basic design goals:

* **plain-text database**: which means you get full access and control over the database.
* **git-integration**: as a benefit of the above, you can keep track of your database through version control.
* **centralized database, location-independent library**: this means, that coBib *only* manages the
  database file in a centralized fashion but allows you to spread the actual contents of your
  library across the entire file system (this is the major different to
  [papis](https://papis.readthedocs.io/en/latest/library_structure.html)).
* **command-line and TUI support**: all features are available through the command-line as well as a curses-based TUI.


### **News:** coBib v4.0 will come with a new UI!
The plan is to switch to [rich][rich] and [textual][textual] instead of the current curses TUI.
This will open up some great possibilities for a much more modern UI.

However, this change will require some *major* refactoring including breaking changes of the API
and some of the user configuration options. It will also be a rather drastic change in style.
Thus, I will attempt to support v3.5 with bugfix releases until 1.1.2023

It will likely take a few months until v4.0 gets released but I am starting development on it now.
You can follow the progress here: <https://gitlab.com/mrossinek/cobib/-/issues/78>

[rich]: https://github.com/Textualize/rich
[textual]: https://github.com/Textualize/textual

## Installation

For all common purposes you can install coBib via `pip`:

```
pip install cobib
```

Note: Use `pip3` if you still have Python 2 installed.

If you would also like to install the man-page and (crude!) Zsh completion,
you need to download the source code and do the following:

```
git clone https://gitlab.com/mrossinek/cobib
cd cobib
make install_extras
```

### Arch Linux

coBib is packaged in the AUR.
* [cobib](https://aur.archlinux.org/packages/cobib/)
* [cobib-git](https://aur.archlinux.org/packages/cobib-git/)

### Windows

Windows is **only partially** supported!
This is due to the fact that [Python under Windows does not ship with the `curses` module][1].
Thus, you cannot run coBib's _TUI_ on Windows.
However, if you are using Windows 10 you should be able to install and use coBib's full
functionality within the Linux subsystem.


## Getting started

To get started, you must initialize the database:

```
cobib init
```

If you would like to enable the git-integration, you should run:

```
cobib init --git
```

*and* enable `config.database.git` (see also [configuration](#configuration)).

Be sure to check out my [Quickstart blog post](https://mrossinek.gitlab.io/programming/introducing-cobib/)
for a more guided introduction compared to the following section!

### Importing your library

coBib provides an `import` command through which you can easily import your library
from another bibliography manager. For more details check out:

```
cobib import --help
```

So far, coBib knows how to import your library from Zotero by simply running:

```
cobib import --zotero
```

Check out the following command, the man page or the online documentation for more details:

```
cobib import --zotero -- --help
```

## Usage

### Adding new entries

You can now add new entries to your database (see also `cobib.commands.add`[^1]):

```
cobib add --bibtex some_biblatex_file.bib
cobib add --arxiv <some arXiv ID>
cobib add --doi <some DOI>
cobib add --isbn <some ISBN>
```

**Note**: when adding data from a `.bib` file, make sure that it is in the Bib**La**Tex format!

### Viewing your database and entries

You can view the contents of your database with (see also `cobib.commands.list`):

```
cobib list
```

You can show a specific entry with (see also `cobib.commands.show`):

```
cobib show <some entry label>
```

You can open an associated file of an entry with (see also `cobib.commands.open`):

```
cobib open <some entry label>
```

You can even search through your database with (see also `cobib.commands.search`):

```
cobib search "some text"
```

### Editing your database

You can delete an entry with (see also `cobib.commands.delete`):

```
cobib delete <some entry label>
```

You can edit an entry manually with (see also `cobib.commands.edit`):

```
cobib edit <some entry label>
```

You can also apply simple modifications to multiple entries at once with (see also
`cobib.commands.modify`):

```
cobib modify tags:private -- <some entry label> <another entry label> ...
```

### Exporting your database

You can export your database with (see also `cobib.commands.export`):

```
cobib export --bibtex my_bibliography.bib
cobib export --zip my_library.zip
```

### Integrated version control

If you have enabled the git-integration, you can undo and re-apply changes to your database with
(see also `cobib.commands.undo` and `cobib.commands.redo`):

```
cobib undo
cobib redo
```

### Getting help

Each subcommand provides additional help via:

```
cobib <subcommand> --help
```

and you can find extensive information in the online documentation (linked above) and the man-page:

```
man cobib
```

### TUI

Finally, you can also use coBib's TUI for a more interactive experience (see also `cobib.tui`), by
simply typing

```
cobib
```


## Configuration

You can overwrite the default configuration by placing a `config.py` file in `~/.config/cobib/`.
The easiest way to get started with this file is by copying [`example.py`](https://gitlab.com/mrossinek/cobib/-/blob/master/src/cobib/config/example.py)
or by using:

```
cobib _example_config > ~/.config/cobib/config.py
```

You can then modify it to your liking.

You may also specify a different config file at runtime by using the `-c` or `--config` command line argument or by specifying a custom path in the `COBIB_CONFIG` environment variable.
You can also disable loading of _any_ configuration file be setting this environment variable to one of the following values: `"", 0, "f", "false", "nil", "none"`.

Finally, be sure to take a look at the man page (`man cobib`) and/or the online documentation for more information.


## Documentation

coBib's documentation is hosted [here](https://mrossinek.gitlab.io/cobib/cobib.html).

If you would like to generate a local version during development, you need to clone the source code, and install [`pdoc`](https://github.com/mitmproxy/pdoc) in order to generate it:

```
git clone https://gitlab.com/mrossinek/cobib.git
cd cobib
pip install pdoc
pdoc -d google -e cobib=https://gitlab.com/mrossinek/cobib/-/blob/master/src/cobib/ -t html -o docs src/cobib tests
```

You can then browse the documentation from `docs/cobib.html`.


## History

I have started this project when I was looking into alternatives to popular reference managers such as Mendeley,
which has more features than I use on a regular basis and does not allow me to work from the command line which is where I spent most of the time that I spent on the computer.

Hence, I have decided to make it my own task of implementing a simple, yet fast, reference manager.
coBib is written in Python and uses a YAML file to store its bibliography in a plain text format.

### Changelog

You can find the detailed changes throughout coBib's history in [the Changelog](https://gitlab.com/mrossinek/cobib/-/blob/master/CHANGELOG.md).


## License

coBib is licensed under the [MIT License](https://gitlab.com/mrossinek/cobib/-/blob/master/LICENSE.txt).

[^1]: References like this one get interpreted by the documentation generator. If you are reading this as the README page, you may find the [online documentation](https://mrossinek.gitlab.io/cobib/cobib.html) more enjoyable.

[1]: https://docs.python.org/3/howto/curses.html#what-is-curses

[//]: # ( vim: set ft=markdown: )
