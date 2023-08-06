from pathlib import Path
import re


__version__ = '0.1.5'
_ENCODING = 'utf-8'


def write(file, s, overwrite=True):
    """ Open file for write mode, write string to it, then close.

    Write string to file in ``utf-8`` encoding.

    If the file already exists, overwrite that by default,
    or FileExistsError if overwrite parameter set to False.

    Parameters
    ----------
    file: str or os.PathLike
        File to write to.
    s: str
        A string to write to file.
    overwrite: bool, default=True
        Overwrite file with s, instead of raise FileExistsError.
        The default value is True, so you should specify this parameter to False
        if you want to use this function safely.

    Returns
    -------
    int
        Character count that were written to file.

    Raises
    ------
    FileExistsError:
        If file already exists and overwrite set to False.
    PermissionError
        Could not open or create file due to permission problem.
    IsADirectoryError
        A value specified to file parameter was a directory.
    TypeError
        Illegal type of parameter specified.

    Examples
    --------

    .. code-block:: python

        textfile.write("a.txt", "any string value")

    This code will write "any string value" to ``a.txt`` file.
    """
    with open(file, 'w', encoding=_ENCODING) as writer:
        writer.write(s)


def append(file, s):
    """ Open file for appending mode, write or append to it, then close.

    Append string to file in ``utf-8`` encoding.

    If the file not exists yet, the behavior is same to write() function.

    Parameters
    ----------
    file: str or os.PathLike
        File to append to.
    s: str
        A string to append to file.

    Returns
    -------
    int
        Character count that were written to file.

    Raises
    ------
    PermissionError
        Could not open or create file due to to permission problem.
    IsADirectoryError
        A value specified to file parameter was a directory.
    TypeError
        Illegal type of parameter specified.

    Examples
    --------
    .. code-block:: python

        textfile.append("a.txt", "str to append")

    This code will append "str to append" to the end of the content of ``a.txt`` file.
    """
    file = Path(file)

    if not file.exists():
        write(file, s)
    else:
        with open(file, 'a', encoding=_ENCODING) as appender:
            appender.write(s)


def prepend(file, s):
    raise NotImplemented()


def insert(file, s, line):
    """ Read content from file, and Write text inserted content to file.

    This function does:

    1. Read Content
        * Open file in read mode.
        * Read content.
        * Close file.
    2. Insert text
        * insert s parameter text at line parameter position.
    3. Write Content
        * Open file in write mode.
        * Write content.
        * Close file.

    Parameters
    ----------
    file: str or os.PathLike
        File to operate.
    s: str
        Text to insert.
    line: int
        Line position.

    Examples
    --------

    This is an example of insert csv file header line.

    >>> textfile.read('a.csv')
    1,Tom,53
    2,Mike,55,
    3,Bob,61
    >>> textfile.insert('a.csv', 'Id,Name,Age\\n', 0)
    >>> textfile.read('a.csv')
    Id,Name,Age
    1,Tom,53
    2,Mike,55,
    3,Bob,61

    And line parameter can be set to negative value.
    If do so, it will be regarded as line position from last of content.

    >>> textfile.insert('a.csv', '\\n4,Jack,31', -1)
    >>> textfile.read('a.csv')
    Id,Name,Age
    1,Tom,53
    2,Mike,55,
    3,Bob,61
    4,Jack,31

    """
    file = Path(file)

    lines = []
    with open(file) as reader:
        for l in reader:
            lines.append(l)

    if line == len(lines) or line == -1:
        lines.append(s)
    else:
        if line < 0:
            line += 1
        lines[line] = s + lines[line]

    file.write_text(''.join(lines))


def head(file, lines):
    raise NotImplemented()


def tail(file, lines):
    raise NotImplemented()


def read(file, silent=False):
    """ Open file for read mode, read string from it, then close.

    Read string from a file with the assumption that it is encoded in ``utf-8``.

    If the file not exists, raise FileNotFoundError, or get empty string as return value
    if silent parameter set to True.

    Parameters
    ----------
    file: str or os.PathLike
        File to read from.
    silent: bool, default=False
        If set to True, read empty string when file not exists.
        If set to False, raise FileNotFoundError when file not exists.

    Returns
    -------
    str
        Read string.

    Raises
    ------
    FileNotFoundError
        File is not exist and silent parameter set to False.
    PermissionError
        Could not open or create file due to permission problem.
    IsADirectoryError
        A value specified to file parameter was a directory.
    TypeError
        Illegal type of parameter specified.

    Examples
    --------
    .. code-block:: python

        s = textfile.read("a.txt")

    This code will read whole text from ``a.txt`` file.
    """
    file = Path(file)
    if not file.exists():
        if silent:
            return ''
        else:
            raise FileNotFoundError(str(file))

    with open(file, encoding=_ENCODING) as reader:
        return reader.read()


def replace(file, old, new):
    """ Replace content in file.

    Read entire content from file, replace old string to new one, then overwrite and close.

    Parameters
    ----------
    file: str or os.PathLike
        File its content to replace.
    old: str
        String to be replaced.
    new: str
        String to replace.

    Raises
    ------
    FileNotFoundError
        File is not exist.
    PermissionError
        Could not open or create file due to permission problem.
    IsADirectoryError
        A value specified to file parameter was a directory.
    TypeError
        Illegal type of parameter specified.

    Examples
    --------
    Assume a file ``a.csv`` that has the content in comma separated format, like below::

        Id,Name,Age
        1,Tom,30
        2,Bob,26
        3,Jane,28

    And execute ``textfile.replace()`` function:

    .. code-block:: python

        textfile.replace("a.csv", ",", "\\t")

    After that, the the content of a.csv will be::

        Id\tName\tAge
        1\tTom\t30
        2\tBob\t26
        3\tJane\t28
    """
    s = read(file)
    s = s.replace(old, new)
    write(file, s)
