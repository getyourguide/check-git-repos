import argparse
import git
import os


def get_branch_condition(repo, branch):
    try:
        commits = repo.iter_commits(f"{branch}@{{u}}..{branch}")
        has_commit_lead = next(commits, None)
        if has_commit_lead:
            return "unpushed_changes"
        return None
    except git.exc.GitCommandError as e:
        is_missing_upstream = "no upstream" in e.stderr
        if is_missing_upstream:
            return "missing_upstream"
        raise e


def is_hidden(path):
    return path.startswith(".")


def filter_hidden(directories):
    return [d for d in directories if not is_hidden(d)]


def directories(path, include_hidden):
    directories = []
    for root, dirs, files in os.walk(path):
        if ".git" in dirs:
            directories.append(root)
            dirs[:] = []
        else:
            if not include_hidden:
                dirs[:] = filter_hidden(dirs)

    return directories


def build_args():
    parser = argparse.ArgumentParser(description="Check the status of git repositories in a directory")
    parser.add_argument(
        "path",
        nargs="?",
        help="if given, the directory to start looking from, otherwise the directory will be used",
        default=os.getcwd(),
    )
    parser.add_argument(
        "--include-hidden",
        required=False,
        help="whether to look in hidden directories",
        action="store_true",
    )
    return parser.parse_args()


def main(args=build_args()):
    for d in directories(args.path, args.include_hidden):
        repo_git = f"{d}/.git"
        if os.path.exists(repo_git):
            repo = git.Repo(repo_git)
            status = []

            if len(repo.untracked_files) > 0:
                status.append("untracked_files")
            if repo.is_dirty():
                status.append("dirty_files")

            branch_issues = []
            for branch in repo.heads:
                branch_condition = get_branch_condition(repo, branch)
                # check if there are commits on the branch that aren't on the upstream
                if branch_condition is not None:
                    branch_issues.append(f"{branch} ({branch_condition})")

            if len(branch_issues) > 0:
                branch_issues_string = ", ".join(branch_issues)
                status.append(f"branch_issues: {branch_issues_string}")

            if len(status) > 0:
                message = ", ".join(status)
                print(f"{repo_git}: {message}")


if __name__ == "__main__":
    main()
