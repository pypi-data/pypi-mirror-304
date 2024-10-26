# pylnlst
> CLI tool to automate the creation of symbolic links in a destination directory.

## Why pylnlst?

Many times I find myself creating multiple symbolic links manually using [Nautilus](https://gitlab.gnome.org/GNOME/nautilus) (or similar) and feeling that the process could be automated. When tried to approach such automation using bash I've failed miserably because find a lot of problems when you try to create links containing spaces, brackets, or exclamation marks because it requires escaping such characters.

This tool has been created to address those problems.

The idea is:
+ User creates a file with a list of absolute or relative paths, one per file/folder.
+ User invokes the tool with two arguments: the location of the file list, and the target (base) location where symbolic links will be created.
+ The tool reads the entries from the file, one by one, and creates a symbolic link in the specified target location, pointing to the original file.
+ If a file with the same name already exists, a suffix is added so that there is no name clash. A warning is displayed.

The usage is as follows:

```bash
python pylnlst.py --file-list fILELIST --dst DST_DIR
```

## Dev notes

Most of the script functionality relies on the [Typer](https://github.com/fastapi/typer) framework. Project management relies on [uv](https://github.com/astral-sh/uv), and linting/formatting is done with [Ruff](https://github.com/astral-sh/ruff).

There are currently no tests.

To check that the packaged script works as expected type:

```bash
# you must be in the directory that contains pylnlst package, not
# within pylnlst
$ uv run --directory pylnlst pylnlst --version
```
The application can be built with `uv build` and published with `uv publish`.

To publish to Test PyPI:

```bash
code
```