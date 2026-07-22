import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend(user_skills):

    # Clean user input
    user_skills = user_skills.lower().strip()

    # Convert user skills into one document
    user_document = ",".join(
        [s.strip() for s in user_skills.split(",") if s.strip()]
    )

    # Load career dataset
    df = pd.read_csv("career_path_matrix.csv")   # Change path if needed

    # Create corpus
    documents = df["prerequisites"].tolist()

    # Append user skills
    documents.append(user_document)

    # TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Separate user vector
    career_vectors = tfidf_matrix[:-1]
    user_vector = tfidf_matrix[-1]

    # Cosine Similarity
    similarity_scores = cosine_similarity(user_vector, career_vectors).flatten()

    # Top 5 recommendations
    top_indices = similarity_scores.argsort()[-5:][::-1]

    # User skill set
    user_skill_set = {
        s.strip().lower()
        for s in user_skills.split(",")
        if s.strip()
    }

    recommendations = []

    for index in top_indices:

        career = df.iloc[index]
        score = similarity_scores[index] * 100

        required_skill_set = {
            s.strip().lower()
            for s in career["prerequisites"].split(",")
        }

        matched_skills = user_skill_set & required_skill_set
        missing_skills = required_skill_set - user_skill_set

        matched_count = len(matched_skills)
        required_count = len(required_skill_set)

        # AI Recommendation Message
        if score >= 80:

            message_title = "⭐ Excellent Match!"

            message_description = (
                f"Your profile strongly aligns with this career. "
                f"You already have {matched_count} out of {required_count} required skills."
            )

            if missing_skills:
                message_action = (
                    f"Focus on learning: {', '.join(sorted(missing_skills))}"
                )
            else:
                message_action = (
                    "Amazing! You already possess all the required skills."
                )

        elif score >= 60:

            message_title = "👍 Good Match!"

            message_description = (
                f"You already have {matched_count} out of {required_count} required skills."
            )

            message_action = (
                f"Learning these skills will strengthen your profile: "
                f"{', '.join(sorted(missing_skills))}"
            )

        else:

            message_title = "📚 Learning Path Recommended!"

            message_description = (
                f"You currently have {matched_count} out of {required_count} required skills."
            )

            message_action = (
                f"Start learning: {', '.join(sorted(missing_skills))}"
            )

        recommendation = {
            "career": career["career_path"],
            "score": round(score, 2),
            "message_title": message_title,
            "message_description": message_description,
            "message_action": message_action,
            "matched_count": matched_count,
            "required_count": required_count,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills),
        }

        recommendations.append(recommendation)

    return recommendations