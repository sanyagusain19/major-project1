import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- Fail loudly if the token isn't loaded, instead of silently getting 401s ---
if not GITHUB_TOKEN:
    raise SystemExit(
        "ERROR: GITHUB_TOKEN not found. Check that a .env file exists in this "
        "folder and contains a line like: GITHUB_TOKEN=ghp_yourtokenhere"
    )

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

conn = sqlite3.connect("developer.db")
cursor = conn.cursor()

skills = [
    "Python",
    "Flask",
    "Machine Learning",
    "Data Science",
    "React",
    "Java",
    "JavaScript",
    "Node.js",
    "FastAPI",
    "TensorFlow"
]


def search_users(skill):
    url = "https://api.github.com/search/users"
    params = {"q": skill, "per_page": 20}

    response = requests.get(url, headers=headers, params=params)

    print("Status:", response.status_code)

    if response.status_code != 200:
        # This is where things were failing silently before —
        # now it prints exactly why every time.
        print("GitHub API error:", response.json())
        return []

    return response.json()["items"]


def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    print(f"Could not fetch details for {username}: {response.status_code}")
    return None


def save_developer(data, skill):
    """
    Insert a new developer, or if the username already exists,
    update their record and merge the new skill into their skills list
    instead of ignoring the row.
    """
    username = data["login"]

    # Check if this user already exists and what skills they already have
    cursor.execute("SELECT skills FROM developers WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        # New developer -> INSERT
        cursor.execute("""
            INSERT INTO developers(
                username, name, bio, skills, interests, location,
                followers, following, public_repos, avatar, github_url, language
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            username,
            data.get("name"),
            data.get("bio"),
            skill,
            "",
            data.get("location"),
            data.get("followers"),
            data.get("following"),
            data.get("public_repos"),
            data.get("avatar_url"),
            data.get("html_url"),
            ""
        ))
    else:
        # Existing developer -> UPDATE, merging the skill in if it's new
        existing_skills = [s.strip() for s in (row[0] or "").split(",") if s.strip()]
        if skill not in existing_skills:
            existing_skills.append(skill)
        merged_skills = ", ".join(existing_skills)

        cursor.execute("""
            UPDATE developers
            SET name = ?, bio = ?, skills = ?, location = ?,
                followers = ?, following = ?, public_repos = ?,
                avatar = ?, github_url = ?
            WHERE username = ?
        """, (
            data.get("name"),
            data.get("bio"),
            merged_skills,
            data.get("location"),
            data.get("followers"),
            data.get("following"),
            data.get("public_repos"),
            data.get("avatar_url"),
            data.get("html_url"),
            username
        ))

    conn.commit()


for skill in skills:
    print(f"\nSearching: {skill}")
    users = search_users(skill)

    for user in users:
        details = get_user_details(user["login"])
        if details:
            save_developer(details, skill)
            print("Saved:", details["login"])

conn.close()
print("\nDatabase Updated Successfully!")
