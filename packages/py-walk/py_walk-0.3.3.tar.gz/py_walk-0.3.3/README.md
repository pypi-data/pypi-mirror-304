<p align="center">
    <img src="https://raw.githubusercontent.com/pacha/py-walk/main/docs/logo-header.png" alt="logo">
</p>

py-walk
=======

![Tests](https://github.com/pacha/py-walk/actions/workflows/tests.yaml/badge.svg)
![Type checks](https://github.com/pacha/py-walk/actions/workflows/type-checks.yaml/badge.svg)
![Code formatting](https://github.com/pacha/py-walk/actions/workflows/code-formatting.yaml/badge.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/py-walk.svg)

_Python library to filter filesystem paths based on gitignore-like patterns._

Example:
```python
from py_walk import walk
from py_walk import get_parser_from_text

patterns = """
    **/data/*.bin
    !**/data/foo.bin

    # python files
    __pycache__/
    *.py[cod]
"""

# you can get the filtered paths from a directory
for path in walk("some/directory", ignore=patterns):
    do_something(path)

# ...or check paths against the patterns manually
parser = get_parser_from_text(patterns, base_dir="some/directory")
if parser.match("file.txt"):
    do_something_else()
```

**py-walk** can be useful for applications or tools that work with paths and aim to
offer a `.gitignore` type file to their users. It's also handy for users working
in interactive sessions who need to quickly retrieve sets of paths that must
meet relatively complex constraints.

> py-walk tries to achieve 100% compatibility with Git's gitignore (wildmatch)
> pattern syntax. Currently, it includes more than 500 tests, which incorporate
> all the original tests from the Git codebase. These tests are executed against
> `git check-ignore` to ensure as much compatibility as possible. If you find
> any divergence, please don't hesitate to open an issue or PR.

## Installation

To install py-walk, simply use `pip`:
```shell
$ pip install py-walk
```

## Usage

With py-walk, you have the ability to input paths into the library to determine
whether they match with a set of gitignore-based patterns. Alternatively, you
can directly traverse the contents of a directory, based on a set of conditions
that the paths must meet.

### walk

To walk through all the contents of a directory, don't provide any constraints:
```python
from py-walk import walk

for path in walk("/some/directory/"):
    print(path)
```
`walk` accepts the directory to traverse as a strings or as a `Path` object from
`pathlib`. It returns `Path` objects.

> `walk` returns a generator, if you prefer to get the results as a list or
> tuple, wrap the call with the desired data type constructor
> (eg. `list(walk("some-dir"))`).

To ignore certain paths, you can pass patterns as a text or a list of patterns:
```python
ignore = """
    # these patterns use gitignore syntax
    foo.txt
    /bar/**/*.dat
"""

for path in walk("/some/directory", ignore=ignore):
    ...
```
or
```python
ignore = ["foo.txt", "/bar/**/*.dat"]
for path in walk("/some/directory", ignore=ignore):
    ...
```

To only retrieve paths that match a set of patterns, use the `match` parameter
(again, passing a text blob or a list of patterns):
```python
for path in walk("/some/directory", ignore=["data/"], match=["*.css", "*.js"]):
    ...
```
> Note that the `ignore` parameter has precedence: once a path is ignored it
> can't be reincluded using the `match` parameter due to performance reasons.
> That includes children of ignored directories. For example, if you ignore
> a directory `/foo/`, `/foo/bar/file.txt` will be ignored even if `match`
> includes the `*.txt` pattern.

In addition, you can retrieve either only files or only directories using the
`mode` parameter:
```python
for path in walk("/some/directory", ignore=["static/"], mode="only-files"):
    ...
```
```python
for path in walk("/some/directory", ignore=["static/"], mode="only-dirs"):
    ...
```

You can combine `ignore`, `match` and `mode` to get the exact list of files
that you need. However, always remember that `ignore` takes precedence over the
other two.

> Note: you can convert any text containing gitignore-based patterns into a list using
> the `py_walk.pattern_text_to_pattern_list` function:
> ```python
> from py_walk import pattern_text_to_pattern_list
>
> pattern_list = pattern_text_to_pattern_list("""
>     # some patterns
>     **/foo.txt
>     dir[A-Z]/
> """)

### get_parser_from_*

You can also create a parser from a gitignore-type text, a list of patterns or
a file handle to a `.gitignore` type of file. Using the `match` method of the
parser, you can directly evaluate paths.

```python
from py_walk import get_parser_from_file

parser = get_parser_from_file("path/to/gitignore-type-file")
if parser.match("file.txt"):
    print("file.txt matches!")
```

```python
from py_walk import get_parser_from_text

patterns = """
# some comment
*.txt
**/bar/*.dat
"""

parser = get_parser_from_text(patterns, base_dir="/some/folder")
if parser.match("file.txt"):
    print("file.txt matches!")
```

```python
from py_walk import get_parser_from_list

patterns = [
    "*.txt",
    "**/bar/*.dat",
]

parser = get_parser_from_list(patterns, base_dir="/some/folder")
if parser.match("file.txt"):
    ...
```

#### base_dir

The `base_dir` denotes the directory where files are stored. When you use
`get_parser_from_file`, the `base_dir` is determined by the location of the
gitignore-type file passed as a parameter. Specifically, it's set to the parent
directory, which mirrors the functionality of Git and a `.gitignore` file.

When using `get_parser_from_text` or `get_parser_from_list`, you have the
option to either explicitly set the `base_dir` or leave it out. If omitted,
most matches will work just fine, as the provided path will simply be compared
to the patterns in a textual manner. However, there are certain instances where
the package will need to access the actual file system to resolve a match. For
instance, if you have a pattern like `foo/bar/` and the provided path is
`foo/bar`, a match will only occur if `bar` is a directory. If `base_dir` is
defined, the package will verify the existence of `bar` and confirm if it is
indeed a directory, returning `True` in that case. If `bar` is not a directory
or `base_dir` is not defined, the result will be `False`. Therefore, while it's
entirely possible to match patterns without a `base_dir`, be mindful of the
potential differences in results. This behavior is directly copied from Git to
maintain as much compatibility with it as possible.

## License

py-walk is available under the MIT license.
