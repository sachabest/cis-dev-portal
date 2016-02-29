import requests

BASE_RUL = "https://api.github.com"

def github_get_request(token, endpoint):
    req = requests.get(BASE_RUL + endpoint)
    req.headers["Authorization"] = token
    if req.status_code != 200:
        raise Exception("GitHub returned improper status code: %d on request to %s"
            % req.status_code, endpoint)
    else:
        return req.json()

def get_org_repos(token, org_name):
    return github_get_request(token, "/orgs/:" + org_name + "/repos")

def get_repo_contributors
# Move these to environment file when appropriate 