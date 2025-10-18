# Movie Recommender

This repository contains a Streamlit-based movie recommender app.

Quick notes before deploying:

- The app expects `movie_list.pkl` and `similarity.pkl` next to `app.py`. Do not commit large binary data files if they are private; keep them local or use an external storage (S3, Azure Blob, etc.).
- Set the TMDB API key in the environment variable `TMDB_API_KEY` to enable poster images. Without it, the app will show placeholder images.

Deploy to Heroku (example):

1. Create a Heroku app and add a Git remote, or use an existing GitHub repo.
2. Ensure `Procfile` and `requirements.txt` are present. This project already contains a `Procfile` and `requirements.txt`.
3. Commit and push:

   git add .
   git commit -m "Prepare app for deployment: remove hard-coded secrets, add .gitignore and README"
   git push heroku main

Deploy to GitHub Pages / Actions or other platforms: follow the platform's Python/Streamlit deployment steps.

Local run:

- Create a virtualenv, install requirements, set `TMDB_API_KEY` if you want posters, then run:

  streamlit run app.py

If you want help pushing to a specific remote (GitHub, Heroku), tell me the remote URL or give me permission to set one and I'll run the git commands for you.
