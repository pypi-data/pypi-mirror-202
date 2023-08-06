"""
Logging Module

This module provides functions for reading and writing contents to a file with logging.

This module contains the following functions:

    * read_contents - returns the contents of a file
    * write_contents - writes contents to a file

"""

from codebuddie.logging_module import logger
from pathlib import Path


def read_contents(filepath: Path) -> str:
    """
    Returns the contents of a file.

    Parameters
    ----------
    filepath : Path
        The path to the file to read.

    Returns
    -------
    str
        The contents of the file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    if not filepath.exists():
        raise FileNotFoundError(f'File not found: {filepath}')
    with open(filepath, 'r') as f:
        content = f.read()
    logger.info(f'read contents from filepath: {filepath}')
    return content


def write_contents(filepath: Path, content: str) -> int:
    """
    Writes contents to a file.

    Parameters
    ----------
    filepath : Path
        The path to the file to write to.
    content : str
        The contents to write to the file.

    Returns
    -------
    int
        The number of characters written to the file.
    """
    with open(filepath, 'w+') as f:
        size = f.write(content)
    logger.info(f'wrote contents to filepath: {filepath}')
    return size