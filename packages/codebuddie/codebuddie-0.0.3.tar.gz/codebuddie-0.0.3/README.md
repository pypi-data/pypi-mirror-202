# codebuddie: CLI

[![Visit Documentation](https://img.shields.io/badge/documentation-c17hawke-orange)](https://c17hawke.github.io/codebuddie)

[![Author](https://img.shields.io/badge/author-c17hawke-green)](https://github.com/c17hawke)
![Last Commit](https://img.shields.io/github/last-commit/c17hawke/codebuddie)
![Release Date](https://img.shields.io/github/release-date/c17hawke/codebuddie)
![Stars GitHub](https://img.shields.io/github/stars/c17hawke/codebuddie)
![Platform](https://img.shields.io/badge/platform-Visual%20Studio%20Code-blue)
![Language](https://img.shields.io/github/languages/top/c17hawke/codebuddie)
![Size](https://img.shields.io/github/repo-size/c17hawke/codebuddie)

## To install codebuddie -

run the following command in your terminal -

```bash
pip install codebuddie
```

## Now following are the ways you can use codebuddie -

> **NOTE: set `OPENAI_API_KEY` as an environment variable before using `codebuddie`**

It can update code with proper comments, docstring, and module docstrings in the following scenarios:

### 1. If pointed to a local directory. [TODO]

```bash
codebuddie -d path/to/source/directory
```

or

```bash
codebuddie --dir path/to/source/directory
```

or

```bash
codebuddie -d path/to/source/directory -o path/to/destination/directory
```

### 1. If pointed to a github repository. [TODO]

```bash
codebuddie -s link/to/github_repository
```

or

```bash
codebuddie --src link/to/github_repository
```

or

```bash
codebuddie -s link/to/github_repository -o link/to/destination/directory
```
