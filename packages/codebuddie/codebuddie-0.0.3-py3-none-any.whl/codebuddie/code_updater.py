"""
codebuddie

This module provides functions for updating Python code using OpenAI's chatGPT API. 

This module contains the following functions:

    * get_query - returns a formatted docstring for use in Python code
    * openai_content_handler - handles content using OpenAI's chatGPT API
    * apply_openai_transform - applies OpenAI transformations to a Python file
    * code_update - updates Python code using OpenAI's chatGPT API

"""

from codebuddie.logging_module import logger
from codebuddie.utils import read_contents, write_contents
import openai
from openai.error import Timeout
import os
from pathlib import Path
from typing import Union

def get_query(content: str) -> str:
    """
    Returns a formatted docstring for use in Python code.

    Parameters
    ----------
    content : str
        The content to be included in the docstring.

    Returns
    -------
    str
        The formatted docstring.

    """

    docstring_format = """
    for module docstring use following example- 
    '''
    Spreadsheet Column Printer

    This script allows the user to print to the console all columns in the
    spreadsheet. It is assumed that the first row of the spreadsheet is the
    location of the columns.

    This tool accepts comma separated value files (.csv) as well as excel
    (.xls, .xlsx) files.

    This script requires that `pandas` be installed within the Python
    environment you are running this script in.

    This file can also be imported as a module and contains the following
    functions:

        * get_spreadsheet_cols - returns the column headers of the file
        * main - the main function of the script
    '''


    for any class - 
    class Example:
        '''
        Short description of Example class

        ...

        Attributes
        ----------
        att1 : type
            description of att1
        att2 : type
            description of att2 (default value)

        Methods
        -------
        method1(arg1: type, arg2: type=value)
            short description of method1
        '''
    for the mothods of class Example you can follow the example of function below    

    for any function - 
    
    def function(arg1: type, arg2: type=value2):
        '''Shot description of function in online

        long description of function

        Parameters
        ----------
        arg1 : type
            description of arg1
        arg2 : type, optional
            description of arg2 (default to value2)

        Returns
        -------
        type
            what it returns

        Raises [only if present in the function]
        ----------
        ExceptionName
            description of exception
    """

    return f"[style guide: provide a high-quality Python docstring, inline code comments (if necessary), \
        module docstring as described in these examples- \n{docstring_format}\n \
        and return Python code for the following snippet. \
        Your code must adhere to the Python standard style guide with \
        a maximum line length of 127 characters. \
        For module docstring use markdown notations for code, command or options \
        Please note that you \
        must not generate any function from your end and strictly\
        return `__init__.py` file as it is]: CODE:-\n{content}"


def openai_content_handler(content: str, temperature: float = 0.0, timeout: Union[int, float]=100) -> str:
    """
    Handles content using OpenAI's chatGPT API.

    Parameters
    ----------
    content : str
        The content to be handled.
    temperature : float, optional
        The sampling temperature to use for the API request (default is 0.0).
    timeout : Union[int, float], optional
        The maximum time to wait for a response from the API (default is 100s).

    Returns
    -------
    str
        The response from the API.

    Raises
    ------
    Timeout
        If the request takes too long to complete and the server closes the connection.
    Exception
        If any other exception occurs.

    """   
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=temperature,
            timeout=timeout,
            messages=[
                {"role": "user", "content": content}  # out new question
            ]
            )
        return response['choices'][0]['message']['content']
    except Timeout:
        message = "A `Timeout` error indicates that your request took too long \
            to complete and our server closed the connection. \
            This could be due to a network issue, a heavy load on our services,\
            or a complex request that requires more processing time."
        logger.exception(message)
        return f"'''skipping due to {message}'''"
    except Exception as exe:
        logger.exception(f"Exception occurred: {exe}")
        raise exe

def apply_openai_transform(src_path: Path, dst_path: Path, timeout: int) -> None:
    """
    Applies OpenAI transformations to a Python file.

    Parameters
    ----------
    src_path : Path
        The path to the source file.
    dst_path : Path
        The path to the destination file.
    timeout : int
        The maximum time to wait for a response from the API.

    Returns
    -------
    None

    """
    original_content = read_contents(src_path)
    content_with_query = get_query(content=original_content)
    response = openai_content_handler(content=content_with_query, timeout=timeout)
    logger.info(f"Response from openai API: \n{response}")
    size = write_contents(filepath=dst_path, content=response)
    logger.info(f"file: {dst_path} of size: {size} bytes, written successfully!")


def code_update(directory: Path, output_dir: Path, timeout: int) -> None:
    """
    Updates Python code using OpenAI's chatGPT API.

    Parameters
    ----------
    directory : Path
        The path to the directory containing the source files.
    output_dir : Path
        The path to the directory where the updated files will be written.
    timeout : int
        The maximum time to wait for a response from the API.

    Returns
    -------
    None

    """
    src_dir = directory
    dst_dir = output_dir

    # Create the destination directory if it doesn't exist
    if not dst_dir.exists():
        dst_dir.mkdir()

    # Iterate over the directories and files in the source directory and its subdirectories
    for dirpath, _, filenames in os.walk(src_dir):
        # Get the corresponding directory path in the destination directory
        dst_dirpath = dst_dir / os.path.relpath(dirpath, src_dir)

        # Create the corresponding directory in the destination directory
        os.makedirs(dst_dirpath, exist_ok=True)

        # Iterate over the Python files in the current directory
        for filename in filenames:
            if filename.endswith(".py"):
                # Get the corresponding file path in the source and destination directories
                src_filepath = os.path.join(dirpath, filename)
                dst_filepath = dst_dirpath / filename

                # Apply the apply_openai_transform to the file and write the
                # transformed content to a new file in the destination directory
                apply_openai_transform(Path(src_filepath), Path(dst_filepath), timeout)