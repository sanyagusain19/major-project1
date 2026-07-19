import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session

from similarity import recommend_by_skills, get_featured_developers
from youtube import search_youtube


load_dotenv()

app = Flask(__name__)

# required for session
app.secret_key = "github_developer_network"


@app.route("/")
def home():
    featured = get_featured_developers(limit=1)
    return render_template("index.html", featured=featured)

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route("/developers")
def developers():
    return render_template("developer.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    skills = request.form.get("skills", "")
    interests = request.form.get("interests", "")


    skills_list = [
        s.strip()
        for s in skills.split(",")
        if s.strip()
    ]


    interests_list = [
        i.strip()
        for i in interests.split(",")
        if i.strip()
    ]


    # save for YouTube recommendations
    session["skills"] = skills_list
    session["interests"] = interests_list


    if not skills_list:
        return render_template(
            "results.html",
            developers=[]
        )


    developer_list = recommend_by_skills(skills_list)


    return render_template(
        "results.html",
        developers=developer_list
    )



@app.route("/youtube")
def youtube():

    skills = session.get("skills", [])
    interests = session.get("interests", [])


    query = " ".join(skills + interests) + " tutorial"


    videos = search_youtube(query)


    return render_template(
        "youtube.html",
        videos=videos
    )



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )