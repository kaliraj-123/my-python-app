from github import Github


def get_repository(repository_url):

    repository_name = repository_url.rstrip("/").split("github.com/")[-1]

    github = Github()

    repository = github.get_repo(repository_name)

    return {
        "name": repository.name,
        "full_name": repository.full_name,
        "url": repository.html_url,
        "default_branch": repository.default_branch,
        "description": repository.description,
        "stars": repository.stargazers_count
    }