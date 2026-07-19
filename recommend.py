import os
import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def search_github_users(skills):

    query = " ".join(skills)

    url = "https://api.github.com/search/users"

    params = {
        "q": query,
        "per_page": 5
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )
    print(response.status_code)
    print(response.json()) 

    users = []

    data = response.json()

    print("Status Code:", response.status_code)
    print("Response:", data)

    if "items" not in data:
        return []

    for item in data["items"]:
        users.append({
        "username": item["login"],
        "profile": item["html_url"],
        "avatar": item["avatar_url"]
    })


    return users
# search_github_users("python")