'''
codebuddie

This module provides a CLI tool to get the files from a directory or 
Github URL and add comments, docstrings, and module docstrings to it. 
It uses OpenAI's GPT-3 to generate the docstrings and comments.

This script requires the following packages mainly to be installed within the 
Python environment you are running this script in:

    * openai
    * dotenv

'''

import argparse 
from pathlib import Path
from codebuddie.downloader import GithubRepoDownloader
from codebuddie import code_update
from codebuddie.logging_module import logger


def main(): # noqa: ANN201
    '''
    CLI to get the files from a directory or Github URL and add comments, 
    docstrings, and module docstrings to it.

    Raises
    ------
    OpenaiApiKeyException
        If OpenAI API key is not set or not specified.
    '''

    parser = argparse.ArgumentParser(
        description="CLI to get the files from a directory or Github URL and add comments, docstrings, and module docstrings to it."
    )


    parser.add_argument(
        "--local_src", "-l",
        help=("Path to the directory of LOCAL source code")
    )

    parser.add_argument(
        "--output", "-o",
        help=("The path to output directory"),
        default="artifacts"
    )

    parser.add_argument(
        "--github_url", "-g",
        help=("Github URL of the repository containing the source code")
    )

    parser.add_argument(
        "--github_src", "-s",
        help=("directory to be updated in the repository containing the source code"),
        default="src"
    )

    parser.add_argument(
        "--timeout", "-t",
        help=("number of seconds to wait for timeout"),
        default=100,
        type=int
    )

    # Parse the arguments
    args = parser.parse_args()

    output_dir = Path(args.output)
    github_src = Path(args.github_src)

    # Check if a local source directory or a Github URL was provided
    if (args.local_src is not None) and (args.github_url is None):
        # Use local source directory
        code_update(directory=Path(args.local_src), output_dir=output_dir, timeout=args.timeout)

    elif (args.github_url is not None):
        # Use Github URL
        downloader = GithubRepoDownloader(
            artifacts_dir=output_dir,
            branch_name="main",
            depth=1,
            github_url=args.github_url)
        if downloader.is_github_url_valid(url=args.github_url):
            logger.info("Repo is valid URL, proceeding further")
        downloader.download_directory()

        code_update(directory=github_src, output_dir=output_dir/"updated", timeout=args.timeout)

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as exe:
        logger.exception(exe)
        raise exe