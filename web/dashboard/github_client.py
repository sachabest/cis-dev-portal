import requests
import urllib

BASE_RUL = "https://api.github.com"

def send_authentication_challenge(data):
    url = "https://github.com/login/oauth/access_token"
    headers = {
        'Accept' : 'application/json'
    }
    url += "?" + urllib.parse.urlencode(data)
    req = requests.post(url, headers=headers)
    if req.status_code != 200:
        raise Exception("GitHub returned improper status code: %d on request to %s. Error: %s"
            % (req.status_code, url, req.text))
    return req.json()['access_token']

def github_get_request(token, endpoint):
    headers = {"Authorization" : 'token ' + token}
    req = requests.get(BASE_RUL + endpoint, headers=headers)
    if req.status_code != 200:
        raise Exception("GitHub returned improper status code: %d on request to %s. Error: %s"
            % (req.status_code, endpoint, req.json()))
    else:
        return req.json()

def get_org_repos(token, org_name):
    return github_get_request(token, "/orgs/" + org_name + "/repos")

def get_repo_contributors(token, org_name, repo_name):
    return github_get_request(token, "/repos/" + org_name + "/" + repo_name + "/contributors")

def github_populate_information(student):
    json = github_get_request(student.github_token, "/user")
    student.github_username = json["login"]
    student.avatar = json["avatar_url"]