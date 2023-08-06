"""coBib's configuration.

This file contains both, the actual implementation of the `Config` class, as well as the runtime
`config` object, which gets exposed on the module level as `cobib.config.config`.
Note, that this last link will not point to the correct location in the online documentation due to
the nature of the lower-level import.
"""

import copy
import importlib.util
import io
import logging
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, TextIO, Union

from cobib.utils.rel_path import RelPath

LOGGER = logging.getLogger(__name__)

ANSI_COLORS = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]


class LabelSuffix(Enum):
    """Suffixes to disambiguate Entry labels."""

    ALPHA = lambda count: chr(96 + count)  # pylint: disable=unnecessary-lambda-assignment
    CAPTIAL = lambda count: chr(64 + count)  # pylint: disable=unnecessary-lambda-assignment
    # pylint: disable=unnecessary-lambda,unnecessary-lambda-assignment
    NUMERIC = lambda count: str(count)


class Config(Dict[str, Any]):
    """coBib's configuration class.

    This class wraps the `dict` type and exposes the dictionary keys as attributes to ease access
    (for both, getting and setting).
    Furthermore, nested attributes can be set directly without having to ensure that the parent
    attribute is already present.

    References:
        [Recursively access dict via attributes](https://stackoverflow.com/a/3031270)
    """

    XDG_CONFIG_FILE: str = "~/.config/cobib/config.py"
    """The XDG-based standard configuration location."""

    DEFAULTS: Dict[str, Any] = {
        "logging": {
            "cache": "~/.cache/cobib/cache",
            "logfile": "~/.cache/cobib/cobib.log",
            "version": "~/.cache/cobib/version",
        },
        "commands": {
            "edit": {
                "default_entry_type": "article",
                "editor": os.environ.get("EDITOR", "vim"),
            },
            "open": {
                "command": "xdg-open" if sys.platform.lower() == "linux" else "open",
                "fields": ["file", "url"],
            },
            "search": {
                "grep": "grep",
                "grep_args": [],
                "ignore_case": False,
            },
        },
        "database": {
            "file": "~/.local/share/cobib/literature.yaml",
            "format": {
                "label_default": "{label}",
                "label_suffix": ("_", LabelSuffix.ALPHA),
                "suppress_latex_warnings": True,
            },
            "git": False,
            "stringify": {
                "list_separator": {
                    "file": ", ",
                    "tags": ", ",
                    "url": ", ",
                },
            },
        },
        "events": {},
        "parsers": {
            "bibtex": {
                "ignore_non_standard_types": False,
            },
            "yaml": {
                "use_c_lib_yaml": False,
            },
        },
        "tui": {
            "default_list_args": ["-l"],
            "prompt_before_quit": True,
            "reverse_order": True,
            "scroll_offset": 3,
            "colors": {
                "cursor_line_fg": "white",
                "cursor_line_bg": "cyan",
                "top_statusbar_fg": "black",
                "top_statusbar_bg": "yellow",
                "bottom_statusbar_fg": "black",
                "bottom_statusbar_bg": "yellow",
                "search_label_fg": "blue",
                "search_label_bg": "black",
                "search_query_fg": "red",
                "search_query_bg": "black",
                "popup_help_fg": "white",
                "popup_help_bg": "green",
                "popup_stdout_fg": "white",
                "popup_stdout_bg": "blue",
                "popup_stderr_fg": "white",
                "popup_stderr_bg": "red",
                "selection_fg": "white",
                "selection_bg": "magenta",
            },
            "key_bindings": {
                "prompt": ":",
                "search": "/",
                "help": "?",
                "add": "a",
                "delete": "d",
                "edit": "e",
                "filter": "f",
                "import": "i",
                "modify": "m",
                "open": "o",
                "quit": "q",
                "redo": "r",
                "sort": "s",
                "undo": "u",
                "select": "v",
                "wrap": "w",
                "export": "x",
                "show": "ENTER",
            },
        },
        "utils": {
            "file_downloader": {
                "default_location": "~/.local/share/cobib",
                "url_map": {},
            },
            "journal_abbreviations": [],
        },
    }
    """The default settings."""

    # pylint: disable=super-init-not-called
    def __init__(self, value: Optional[Dict[str, Any]] = None) -> None:
        """Initializer of the recursive, attribute-access, dict-like configuration object.

        The initializer does nothing when `None` is given.
        When a dict is given, all values are set as attributes.

        Args:
            value: a dictionary of settings.
        """
        if value is None:
            pass
        elif isinstance(value, dict):
            self.update(**value)
        else:
            raise TypeError("expected dict")

    def __setitem__(self, key: str, value: Any) -> None:
        """Sets a key, value pair in the object's dictionary.

        Args:
            key: the attributes' name.
            value: the attributes' value.
        """
        if isinstance(value, dict) and not isinstance(value, Config):
            value = Config(value)
        super().__setitem__(key, value)

    def __setattr__(self, key: str, value: Any) -> None:
        """Use `__setitem__` to set attributes unless it is a private (`__`) field.

        This is necessary in order to avoid a RecursionError during the pdoc generation.

        Args:
            key: the attributes' name.
            value: the attributes' value.
        """
        if key[0:2] == "__":
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    MARKER = object()
    """A helper object for detecting the nested recursion-threshold."""

    EXCEPTIONAL_KEYS = {"events", "url_map"}
    """A set of exceptional keys which do not cause automatic item creation. This is required in
    order to support `dict`-like configuration options properly."""

    def __getitem__(self, key: str) -> Any:
        """Gets a key from the configuration object's dictionary.

        If the key is not present yet, it is automagically initialized with an empty configuration
        object to allow recursive attribute-setting.

        Args:
            key: the queried attributes' name.

        Returns:
            The value of the queried attribute.
        """
        found = self.get(key, Config.MARKER)
        if found is Config.MARKER and key not in Config.EXCEPTIONAL_KEYS:
            found = Config()
            super().__setitem__(key, found)
        return found

    def __getattr__(self, key: str) -> Any:
        """Use `__getitem__` to get attributes unless it is a private (`__`) field.

        This is necessary in order to avoid a RecursionError during the pdoc generation.

        Args:
            key: the queried attributes' name.

        Returns:
            The value of the queried attribute.
        """
        if key[0:2] == "__":
            return self.get(key)
        return self.__getitem__(key)

    def update(self, **kwargs) -> None:  # type: ignore
        """Updates the configuration with a dictionary of settings.

        This function ensures values are deepcopied, too.

        Args:
            kwargs: key, value pairs to be added to the configuration data.
        """
        for key, value in kwargs.items():
            self[key] = copy.deepcopy(value)

    @staticmethod
    def load(configpath: Optional[Union[str, Path, TextIO, io.TextIOWrapper]] = None) -> None:
        """Loads another configuration object at runtime.

        WARNING: The new Python-like configuration allows essentially arbitrary Python code so it is
        the user's responsibility to treat this with care!

        Args:
            configpath: the path to the configuration.
        """
        if configpath is not None:
            if isinstance(configpath, (TextIO, io.TextIOWrapper)):
                configpath = configpath.name
        elif "COBIB_CONFIG" in os.environ:
            configpath_env = os.environ["COBIB_CONFIG"]
            if configpath_env.lower() in ("", "0", "f", "false", "nil", "none"):
                LOGGER.info(
                    "Skipping configuration loading because negative COBIB_CONFIG environment "
                    "variable was detected."
                )
                return
            configpath = RelPath(configpath_env).path
        elif RelPath(Config.XDG_CONFIG_FILE).exists():
            configpath = RelPath(Config.XDG_CONFIG_FILE).path
        else:  # pragma: no cover
            return  # pragma: no cover
        LOGGER.info("Loading configuration from default location: %s", configpath)

        spec = importlib.util.spec_from_file_location("config", configpath)
        if spec is None:
            LOGGER.error(
                "The config at %s could not be interpreted as a Python module.", configpath
            )
            sys.exit(1)
        else:
            cfg = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cfg)  # type: ignore

        try:
            # validate config
            config.validate()
        except RuntimeError as exc:
            LOGGER.error(exc)
            sys.exit(1)

    def validate(self) -> None:
        """Validates the configuration at runtime.

        Raises:
            RuntimeError when an invalid setting is encountered.
        """
        LOGGER.info("Validating the runtime configuration.")

        # LOGGING section
        LOGGER.debug("Validating the LOGGING configuration section.")
        self._assert(
            isinstance(self.logging.cache, str), "config.logging.cache should be a string."
        )
        self._assert(
            isinstance(self.logging.logfile, str), "config.logging.logfile should be a string."
        )
        self._assert(
            self.logging.version is None or isinstance(self.logging.version, str),
            "config.logging.version should be a string or `None`.",
        )

        # COMMANDS section
        LOGGER.debug("Validating the COMMANDS configuration section.")
        # COMMANDS.EDIT section
        LOGGER.debug("Validating the COMMANDS.EDIT configuration section.")
        self._assert(
            isinstance(self.commands.edit.default_entry_type, str),
            "config.commands.edit.default_entry_type should be a string.",
        )
        self._assert(
            isinstance(self.commands.edit.editor, str),
            "config.commands.edit.editor should be a string.",
        )
        # COMMANDS.OPEN section
        LOGGER.debug("Validating the COMMANDS.OPEN configuration section.")
        self._assert(
            isinstance(self.commands.open.command, str),
            "config.commands.open.command should be a string.",
        )
        self._assert(
            isinstance(self.commands.open.fields, list),
            "config.commands.open.fields should be a list.",
        )
        # COMMANDS.SEARCH section
        LOGGER.debug("Validating the COMMANDS.SEARCH configuration section.")
        self._assert(
            isinstance(self.commands.search.grep, str),
            "config.commands.search.grep should be a string.",
        )
        self._assert(
            isinstance(self.commands.search.grep_args, list),
            "config.commands.search.grep_args should be a list.",
        )
        self._assert(
            isinstance(self.commands.search.ignore_case, bool),
            "config.commands.search.ignore_case should be a boolean.",
        )

        # DATABASE section
        self._assert(
            isinstance(self.database.file, str), "config.database.file should be a string."
        )
        self._assert(
            isinstance(self.database.git, bool), "config.database.git should be a boolean."
        )
        # DATABASE.FORMAT section
        if "month" in self["database"]["format"].keys():
            LOGGER.warning(
                "The config.database.format.month setting is deprecated as of version 3.1.0! "
                "Instead, coBib will store the month as a three-letter code which is a common "
                "format for which most citation styles include macros. See also "
                "https://www.bibtex.com/f/month-field/"
            )
        self._assert(
            isinstance(self.database.format.label_default, str),
            "config.database.format.label_default should be a string.",
        )
        self._assert(
            isinstance(self.database.format.label_suffix, tuple)
            and len(self.database.format.label_suffix) == 2,
            "config.database.format.label_suffix should be a tuple of length 2.",
        )
        self._assert(
            isinstance(self.database.format.label_suffix[0], str),
            "The first entry of config.database.format.label_suffix should be a string.",
        )
        self._assert(
            callable(self.database.format.label_suffix[1]),
            "The first entry of config.database.format.label_suffix should be a function.",
        )
        self._assert(
            isinstance(self.database.format.suppress_latex_warnings, bool),
            "config.database.format.suppress_latex_warnings should be a boolean.",
        )
        self._assert(
            isinstance(self.database.stringify.list_separator.file, str),
            "config.database.stringify.list_separator.file should be a string.",
        )
        self._assert(
            isinstance(self.database.stringify.list_separator.tags, str),
            "config.database.stringify.list_separator.tags should be a string.",
        )
        self._assert(
            isinstance(self.database.stringify.list_separator.url, str),
            "config.database.stringify.list_separator.url should be a string.",
        )

        # EVENTS section
        self._assert(isinstance(self.events, dict), "config.events should be a dict.")
        for event in self.events:
            self._assert(
                event.validate(),
                f"config.events.{event} did not pass its validation check.",
            )

        # PARSER section
        self._assert(
            isinstance(self.parsers.bibtex.ignore_non_standard_types, bool),
            "config.parsers.bibtex.ignore_non_standard_types should be a boolean.",
        )
        self._assert(
            isinstance(self.parsers.yaml.use_c_lib_yaml, bool),
            "config.parsers.yaml.use_c_lib_yaml should be a boolean.",
        )
        if self.parsers.yaml.use_c_lib_yaml is False:
            LOGGER.warning(
                "The config.parsers.yaml.use_c_lib_yaml setting (introduced in version 3.4.0) will "
                "change its default value to `True` in version 4.0.0!"
            )

        # TUI section
        self._assert(
            isinstance(self.tui.default_list_args, list),
            "config.tui.default_list_args should be a list.",
        )
        self._assert(
            isinstance(self.tui.prompt_before_quit, bool),
            "config.tui.prompt_before_quit should be a boolean.",
        )
        self._assert(
            isinstance(self.tui.reverse_order, bool),
            "config.tui.reverse_order should be a boolean.",
        )
        self._assert(
            isinstance(self.tui.scroll_offset, int),
            "config.tui.scroll_offset should be an integer.",
        )

        # TUI.COLORS section
        LOGGER.debug("Validating the TUI.COLORS configuration section.")
        for name in self.DEFAULTS["tui"]["colors"]:
            self._assert(
                name in self.tui.colors.keys(), f"Missing config.tui.colors.{name} specification!"
            )

        for name, color in self.tui.colors.items():
            if name not in self.DEFAULTS["tui"]["colors"] and name not in ANSI_COLORS:
                LOGGER.warning("Ignoring unknown TUI color: %s.", name)
            self._assert(
                bool(
                    (color in ANSI_COLORS)
                    or (
                        len(color.strip("#")) == 6
                        and tuple(int(color.strip("#")[i : i + 2], 16) for i in (0, 2, 4))
                    )
                ),
                f"Unknown color specification: {color}",
            )

        # TUI.KEY_BINDINGS section
        LOGGER.debug("Validating the TUI.KEY_BINDINGS configuration section.")
        for command in self.DEFAULTS["tui"]["key_bindings"]:
            self._assert(
                command in self.tui.key_bindings.keys(),
                f"Missing config.tui.key_bindings.{command} key binding!",
            )
        for command, key in self.DEFAULTS["tui"]["key_bindings"].items():
            self._assert(
                isinstance(key, str), f"config.tui.key_bindings.{command} should be a string."
            )

        # UTILS section
        LOGGER.debug("Validating the UTILS configuration section.")
        self._assert(
            isinstance(self.utils.file_downloader.default_location, str),
            "config.utils.file_downloader.default_location should be a string.",
        )
        self._assert(
            isinstance(self.utils.file_downloader.url_map, dict),
            "config.utils.file_downloader.url_map should be a dict.",
        )
        for pattern, repl in self.utils.file_downloader.url_map.items():
            self._assert(
                isinstance(pattern, str) and isinstance(repl, str),
                "config.utils.file_downloader.url_map should be a dict[str, str].",
            )

        self._assert(
            isinstance(self.utils.journal_abbreviations, list),
            "config.utils.journal_abbreviations should be a list.",
        )
        for abbrev in self.utils.journal_abbreviations:
            self._assert(
                isinstance(abbrev, tuple),
                "config.utils.journal_abbreviations should be a list of tuples.",
            )

    @staticmethod
    def _assert(expression: bool, error: str) -> None:
        """Asserts the expression is True.

        Args:
            expression: the expression to assert.
            error: the message of the `RuntimeError` upon assertion failure.

        Raises:
            RuntimeError with the specified error string.
        """
        if not expression:
            raise RuntimeError(error)

    def defaults(self) -> None:
        """Resets the configuration to the default settings."""
        # pylint: disable=consider-using-dict-items
        for section in self.DEFAULTS:
            if section == "events":
                # manually reset events
                self["events"] = {}
                continue
            self[section].update(**self.DEFAULTS[section])

    def get_ansi_color(self, name: str) -> str:
        r"""Returns an ANSI color code for the named color.

        Appending `_fg` and `_bg` to the color name will yield the configured colors for the fore-
        and background property, respectively.
        The [ANSI color code](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit) can
        then be constructed using the formula `\x1b[{FG};{BG}m`.

        Args:
            name: a named color as specified in the configuration *excluding* the `_fg` or `_bg`
                  suffix.

        Returns:
            A string representing the foreground and background ANSI color code.
        """
        fg_color = 30 + ANSI_COLORS.index(self.tui.colors.get(name + "_fg"))
        bg_color = 40 + ANSI_COLORS.index(self.tui.colors.get(name + "_bg"))

        return f"\x1b[{fg_color};{bg_color}m"


config: Config = Config()
"""This is the runtime configuration object. It is exposed on the module level via:
```python
from cobib.config import config
```
"""
config.defaults()
