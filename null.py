# JUST TO CLEAN STUFF UP, USED CHATGPT

""" import requests
import json
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

API_URL = 'https://api.jikan.moe/v4/anime'
print(API_URL)

################################ NOTE: ISSUES ##################################
#------EXTREMELY SLOW, makes lots of sense as it goes through a damn good amount of data
#something called asynchronous request
#------JIKAN API HAS A RATE LIMIT, should implement that at some point
#would probably help the above issue
################################ NOTE: ISSUES ##################################

################################ NOTE ##################################
#------ return redirect(url_for('index')) #reloads the page
#------ return jsonify(queryJsom) #shows how data looks in a browser

#------ Using .get() instead of ["key"] in case it doesnt exist so it wont crash
# ex use/syntax on deeper by chatgpt: anime.get("images", {}).get("jpg", {}).get("image_url")
#------ Can use loops when getting data, check anime_info object
#------ .get only works on an object and not lists
#------ for (anime.get("demographics") or [{}])[0].get("name"), the prenthesis makes it so that everyhtign
# in the parenthesis runs before anything else in the line can
#------ or is like a fallback thing, refer to anime_info_object['demographics']
################################ NOTE ##################################
currently_watching = []

#time cleaner/converter
def cleaned_duration(duration_str):
    if not duration_str:
        return None

    stripped_duration = duration_str.lower().strip()
    for string in ("per ep", "per episode", "per eps", "per", "each", "episodes", "episode", "~"):
        stripped_duration = stripped_duration.replace(string, " ")
    cleaned = " ".join(stripped_duration.split())
    print('--------cleaned:', cleaned)

    hour_search = re.search(r'(\d+)\s*(?:h|hr|hrs|hour|hours)\b', cleaned)
    minute_search  = re.search(r'(\d+)\s*(?:m|min|mins|minute|minutes)\b', cleaned)
    print('--------hour_search:', hour_search)
    print('--------minute_search:', minute_search)
    if hour_search or minute_search:
        hours = int(hour_search.group(1)) if hour_search else 0
        minutes = int(minute_search.group(1)) if minute_search else 0
        print('--------hours:', hours)
        print('--------minutes:', minutes)

        total_minutes = hours * 60 + minutes
        print('--------total_minutes:', total_minutes)
        return total_minutes

#logic for how long itll take to finish
def finish(anime)
    

#later:  Rate Limit (Jikan API has no authentication but but has rate limit of 3 requests per second) ################################## Highly doubt to go over that but you never know


#NOTE - HOME PAGE ROUTE - ###########################################################################################################
@app.route('/', methods=["GET", "POST"])
def home():

# TODO currently-watching ############################################################################################################
    global currently_watching

# TODO add-anime ################################################################################################################
    
    if request.method == "GET":
        query = request.args.get('name')
        print ('------Search query:', query)

        if query:
            queryJson = requests.get(API_URL, params={'q': query}).json()

            anime_suggestions = []
            for anime in queryJson.get('data', []):
                anime_info = {
                    'title': anime.get("title"),
                    'image': anime.get("images", {}).get("jpg", {}).get("image_url"), 
                        #is jpg but there is webp
                    'type': anime.get("type"),
                    'episodes': anime.get("episodes"),
                    'duration': anime.get("duration"),
                        #NOTE: need this for later, issue is reads as "23 minutes per eps" and not a number
                        #and is not uniform so some says '1hr 52 min' or just plain '10 min'
                        #can I possibly search for specific things there?
                        #weresoscrewed #kms
                    'MALurl': anime.get("url"),
                    'status': anime.get("status"),
                        #I dont know if I need this or not
                    'year': anime.get("year") or anime.get("aired", {}).get("prop", {}).get("from", {}).get("year"),
                    'genres': [g.get("name") for g in anime.get("genres", [])],
                        #makes a list, each "name" becomes an item "g" and the thing loops for each 
                        #"genres" object
                    'demographics': (anime.get("demographics") or [{}])[0].get("name")
                        #gets the first object from list and then gets the name, NOTE: may have to 
                        #rework this later as it is a list which mmight mean their can be multiple 
                        #objects such as genres above, reworked from: 
                        #anime.get("demographics", [{}])[0].get("name"), because it seems I got no 
                        #demographics on something
                    #'trailer': anime.get(), JUST MAYBE
                }
                anime_suggestions.append(anime_info)
            
            #return (jsonify(anime_suggestions))
            return render_template('index.html', anime_suggestions=anime_suggestions)
                #dont know why lists are passed on like that but thats for future me to understand
            
        else:
            return render_template('index.html', currently_watching=currently_watching)
            #Must be render, not redirect
                #When you open your Flask app in a browser (like http://localhost:5006/),
                #the browser automatically sends a GET request — always.


    else:
        duration_minute = cleaned_duration(request.form.get('duration'))
        print('------duration_minute:', duration_minute)
        #currently_watching list already created above
        anime_info = {
            'title': request.form.get('title'),
            'image': request.form.get('image'),
            'episodes': request.form.get('episodes'),
            'duration': request.form.get('duration'),
            'MALurl': request.form.get('MALurl'),
            'year': request.form.get('year'),
            'demographics': request.form.get('demographics'),
            #'genres': request.form.get('genres')
                #dont know how to turn genres into list again yet
        }
        print(anime_info)

        currently_watching.append(anime_info)
            #should be fine calling both anime_info for diff things in if loop, prolly
        print(currently_watching)
        return redirect(url_for('home'))
            #Flask makes another GET request

    

# TODO watched-anime #################################################################################################################

# TODO just-finished #################################################################################################################

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5006) """