import sqlite3
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_by_skills(skills, limit=30):

    conn = sqlite3.connect("developer.db")

    df = pd.read_sql_query("""
        SELECT *
        FROM developers
    """, conn)

    conn.close()

    if df.empty:
        print("WARNING: developers table is empty — run fetch_github.py first")
        return []

    # Create developer profile
    df["profile"] = (
        df["skills"].fillna("") + " " +
        df["bio"].fillna("") + " " +
        df["language"].fillna("") + " " +
        df["location"].fillna("")
    )

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["profile"])

    user_profile = " ".join(skills)
    user_vector = vectorizer.transform([user_profile])

    similarity_scores = cosine_similarity(
        user_vector,
        tfidf_matrix
    ).flatten()

    df["similarity"] = similarity_scores

    # Drop zero-relevance matches, then take the top `limit`
    recommendations = (
        df[df["similarity"] > 0]
        .sort_values(by="similarity", ascending=False)
        .head(limit)
    )

    results = []

    for _, developer in recommendations.iterrows():
        results.append({
            "username": developer["username"],
            "name": developer["name"],
            "bio": developer["bio"],
            "skills": developer["skills"],
            "language": developer["language"],
            "location": developer["location"],
            "followers": developer["followers"],
            "public_repos": developer["public_repos"],
            "avatar": developer["avatar"],
            "profile": developer["github_url"],
            "similarity": round(
                developer["similarity"] * 100,
                2
            )
        })

    return results
def get_featured_developers(limit=1):
    """Pulls top developers by followers for homepage showcase."""
    conn = sqlite3.connect("developer.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM developers
        WHERE followers IS NOT NULL
        ORDER BY followers DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]