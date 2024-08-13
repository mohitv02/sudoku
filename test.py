mohitvermavermamohit


import requests
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

urls = []
repoUrls = []
repoName = []

def search_github_code(query, github_token):
    exact_query = f'"{query}"'
    url = f"https://api.github.com/search/code?q={exact_query}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        code_results = response.json().get('items', [])
        repo_dict = defaultdict(list)
        for result in code_results:
            repo_full_name = result['repository']['full_name']
            repo_dict[repo_full_name].append(result)
            repoName.append(repo_full_name)

        for repo, files in repo_dict.items():
            print(f"Repository: {repo}")
            repoUrls.append(f"https://github.com/{repo}.git")
            print(f"Repository Link: https://github.com/{repo}")
