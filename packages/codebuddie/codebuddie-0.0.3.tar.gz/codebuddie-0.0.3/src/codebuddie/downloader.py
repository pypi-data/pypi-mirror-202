"""
Github Repo Downloader

This module provides a class `GithubRepoDownloader` which can be used 
to download a GitHub repository to a local directory.

Classes
-------
GithubRepoDownloader
    A class to download a GitHub repository to a local directory.

Methods
-------
is_github_url_valid(url: str) -> bool
    Checks if the given URL is a valid GitHub repository URL.

download_directory() -> None
    Downloads the GitHub repository to the local directory.

"""

import os
import re
import shutil
import requests
from pathlib import Path
from git.repo import Repo
from codebuddie.logging_module import logger
from codebuddie.exception_handler import InvalidURLException, GitHubAPIException


class GithubRepoDownloader:
    """
    A class to download a GitHub repository to a local directory.

    Attributes
    ----------
    artifacts_dir : Path
        The local directory where the repository will be downloaded.
    branch_name : str
        The name of the branch to download.
    depth : int
        The depth of the clone.
    github_url : str
        The URL of the GitHub repository to download.
    """

    def __init__(
            self,
            artifacts_dir: Path = Path("artifacts/temp_src_dir"),
            branch_name: str = "main",
            depth: int = 1,
            github_url: str = None):
        """
        Parameters
        ----------
        artifacts_dir : Path, optional
            The local directory where the repository will be downloaded. Default is `Path("artifacts/temp_src_dir")`.
        branch_name : str, optional
            The name of the branch to download. Default is `"main"`.
        depth : int, optional
            The depth of the clone. Default is `1`.
        github_url : str, optional
            The URL of the GitHub repository to download. Default is `None`.
        """
        self.artifacts_dir = artifacts_dir
        self.branch_name = branch_name
        self.depth = depth
        self.github_url = str(github_url)

    @staticmethod
    def is_github_url_valid(url: str) -> bool:
        """
        Checks if the given URL is a valid GitHub repository URL.

        Parameters
        ----------
        url : str
            The URL to check.

        Returns
        -------
        bool
            True if the URL is a valid GitHub repository URL, False otherwise.

        Raises
        ------
        InvalidURLException
            If the URL is not a valid GitHub repository URL.
        GitHubAPIException
            If the repository does not exist.
        """
        # Check if the URL matches the GitHub repository pattern
        pattern = r'^https:\/\/github\.com\/([a-zA-Z0-9-]+)\/([a-zA-Z0-9-]+)$'
        if not re.match(pattern, url):
            raise InvalidURLException(url)

        # Make a GET request to the GitHub API to check if the repository exists
        response = requests.get(url)

        # If the response status code is 404, the repository doesn't exist
        if response.status_code == 404:
            raise GitHubAPIException(url, response.status_code)

        # Otherwise, the repository exists
        return True

    def download_directory(self) -> None:
        """
        Downloads the GitHub repository to the local directory.
        """
        # Clone the repository to the local directory
        try:
            repo = Repo.clone_from(self.github_url, self.artifacts_dir, branch=self.branch_name, depth=self.depth)
            print(repo)
        except Exception as e:
            logger.exception(f"{e}")