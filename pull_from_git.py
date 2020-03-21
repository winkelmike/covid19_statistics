import git


def pull_from_git(repo):
    repo.remotes.origin.pull()


def check_git_status(repo):
    current = repo.head.commit
    repo.remotes.origin.pull()
    return True if current != repo.head.commit else False


if __name__ == "__main__":
    covid_repo = git.Repo("C:\\Users\\mwinkel.DVG\\Desktop\\covid19_statistics\\source_data")
    pull_from_git(covid_repo)
