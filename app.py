import requests
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

API_URL = 'https://api.jikan.moe/v4/anime'

###############################################################################
# NOTES & IMPROVEMENTS
###############################################################################
# - Jikan API is public and rate-limited (3 requests/sec). Consider async requests later.
# - Use `.get()` safely for optional fields to avoid KeyErrors.
# - Returning redirect(url_for('home')) triggers a fresh GET request.
# - jsonify() can be used to inspect JSON responses directly in the browser.
###############################################################################

# This will store current watchlist (in memory only, lost on restart)
currently_watching = []

###############################################################################
# Helper: Convert duration text to total minutes
###############################################################################
def cleaned_duration(duration_str):
    if not duration_str:
        return None

    # Normalize and remove irrelevant words
    stripped = duration_str.lower().strip()
    for s in ("per ep", "per episode", "per eps", "per", "each", "episodes", "episode", "~"):
        stripped = stripped.replace(s, " ")
    cleaned = " ".join(stripped.split())
    print('--------cleaned:', cleaned)

    # Extract hours and minutes using regex
    hour_search = re.search(r'(\d+)\s*(?:h|hr|hrs|hour|hours)\b', cleaned)
    minute_search = re.search(r'(\d+)\s*(?:m|min|mins|minute|minutes)\b', cleaned)

    hours = int(hour_search.group(1)) if hour_search else 0
    minutes = int(minute_search.group(1)) if minute_search else 0
    total_minutes = hours * 60 + minutes

    print('--------total_minutes:', total_minutes)
    return total_minutes


###############################################################################
# Placeholder: Future logic for calculating completion time
###############################################################################
def calculate_finish_time(anime):
    """TODO: Will compute how long until completion based on watch progress."""
    pass


###############################################################################
# ROUTES
###############################################################################
@app.route('/', methods=["GET", "POST"])
def home():
    global currently_watching

    # ----------------------------------------------------
    # GET: Search for anime or show current watchlist
    # ----------------------------------------------------
    if request.method == "GET":
        query = request.args.get('name')
        print('------Search query:', query)

        if query:
            # Fetch anime search results
            query_json = requests.get(API_URL, params={'q': query}).json()
            anime_suggestions = []

            for anime in query_json.get('data', []):
                anime_info = {
                    'title': anime.get("title"),
                    'image': anime.get("images", {}).get("jpg", {}).get("image_url"),
                    'type': anime.get("type"),
                    'episodes': anime.get("episodes"),
                    'duration': anime.get("duration"),
                    'MALurl': anime.get("url"),
                    'status': anime.get("status"),
                    'year': anime.get("year") or anime.get("aired", {}).get("prop", {}).get("from", {}).get("year"),
                    'genres': [g.get("name") for g in anime.get("genres", [])],
                    'demographics': (anime.get("demographics") or [{}])[0].get("name"),
                }
                anime_suggestions.append(anime_info)

            # Render search results
            return render_template('index.html', anime_suggestions=anime_suggestions)

        # If no query, show current watchlist
        return render_template('index.html', currently_watching=currently_watching)

    # ----------------------------------------------------
    # POST: Add anime to "currently watching"
    # ----------------------------------------------------
    else:
        duration_minutes = cleaned_duration(request.form.get('duration'))
        print('------duration_minutes:', duration_minutes)

        anime_info = {
            'title': request.form.get('title'),
            'image': request.form.get('image'),
            'episodes': int(request.form.get('episodes') or 0),
            'duration': duration_minutes,
            'MALurl': request.form.get('MALurl'),
            'year': request.form.get('year'),
            'demographics': request.form.get('demographics'),
            'episodes_watched': 0,  # default new anime progress
        }

        currently_watching.append(anime_info)
        print('------Added anime:', anime_info)
        print('------Currently Watching:', currently_watching)

        # Redirect to trigger a clean GET (avoids form resubmission)
        return redirect(url_for('home'))


###############################################################################
# MAIN ENTRY
###############################################################################
if __name__ == "__main__":
    app.run(debug=True, port=5006)