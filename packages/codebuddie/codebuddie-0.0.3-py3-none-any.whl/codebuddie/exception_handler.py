"""
Custom Exceptions for URL validation, GitHub API and OpenAI API Key errors

This module contains custom exception classes for handling URL validation errors,
GitHub API errors and OpenAI API Key errors.

Classes
-------
InvalidURLException
    Exception raised when an invalid URL is provided.
GitHubAPIException
    Exception raised when a request to the GitHub API fails.
OpenaiApiKeyException
    Exception raised when an invalid OpenAI API key is provided.

"""

class InvalidURLException(Exception):
    """
    Exception raised when an invalid URL is provided.

    Attributes
    ----------
    message : str
        Explanation of the error message.
    """
    def __init__(self, url: str):
        self.message = f'{url} is not a valid URL'
        super().__init__(self.message)


class GitHubAPIException(Exception):
    """
    Exception raised when a request to the GitHub API fails.

    Attributes
    ----------
    message : str
        Explanation of the error message.
    """
    def __init__(self, url: str, status_code: int):
        self.message = f'Request to {url} failed with status code {status_code}'
        super().__init__(self.message)


class OpenaiApiKeyException(Exception):
    """
    Exception raised when an invalid OpenAI API key is provided.

    Attributes
    ----------
    message : str
        Explanation of the error message.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)