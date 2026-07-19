import sqlite3
import requests
import os
from dotenv import load_dotenv
from collections import Counter
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}
conn = sqlite3.connect("developer.db")
cursor = conn.cursor()
cursor.execute("SELECT username FROM developers")
developers = cursor.fetchall()

def get_repos(username):

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(
        url,
        headers=headers,
        params={"per_page":100}
    )

    if response.status_code == 200:
        return response.json()

    return []
for developer in developers:

    username = developer[0]

    print("Checking:", username)

    repos = get_repos(username)

    languages = []

    for repo in repos:

        if repo["language"]:
            languages.append(repo["language"])

    language_counter = Counter(languages)

    top_languages = language_counter.most_common(5)

    language_string = ", ".join(
        language for language, count in top_languages
    )

    cursor.execute("""
        UPDATE developers
        SET language = ?
        WHERE username = ?
    """, (language_string, username))

    conn.commit()
conn.close()

print("Languages Updated Successfully!")