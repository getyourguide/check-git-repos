# check_git_repos

A simple utility script to check git repos contained underneath a given directory, reporting if any of the repos contain changes that
need to be upstreamed.

## Usage

```bash
usage: check_git_repos [-h] [--include-hidden] [path]

Check the status of git repositories in a directory

positional arguments:
  path              if given, the directory to start looking from, otherwise the directory will be used

optional arguments:
  -h, --help        show this help message and exit
  --include-hidden  whether to look in hidden directories
```

## Checked issues:
### Repo level issues:
- `untracked_files` the repo has files which aren't tracked
- `dirty_files` the repo has dirty files which need to be committed

### Branch level issues:
The reporting format is `branch_issues: [branch] ([issue])`

- `missing_upstream` a branch exists that has no upstream
- `unpushed_changes` a branch has commits that don't exist upstream

## Development

The project is built using [poetry](https://github.com/python-poetry/poetry), and has a makefile for development:

- `clean`: clean up build artifacts
- `develop`: install the project to a virtual environment
- `format`: format files using black
- `publish`: publish the project to pypi (given you have credentials)

Once `make develop` is run, you can run the development version with `poetry run check_git_repos`
