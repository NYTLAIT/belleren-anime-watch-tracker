import requests
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

API_URL = 'https://api.jikan.moe/v4/anime'
print(API_URL)


################################ NOTE ##################################
#------ return redirect(url_for('index')) #reloads the page
#------ return jsonify(queryJsom) #shows how data looks in a browser

#------ Using .get() instead of ["key"] in case it doesnt exist so it wont crash
# ex use/syntax on deeper by chatgpt: anime.get("images", {}).get("jpg", {}).get("image_url")
################################ NOTE ##################################

#later:  Rate Limit (Jikan API has no authentication but but has rate limit of 3 requests per second) ################################## Highly doubt to go over that but you never know

#NOTE - HOME PAGE ROUTE - ###########################################################################################################
@app.route('/', methods=["GET", "POST"])
def home():

# TODO currently-watching ############################################################################################################


# TODO add-anime ################################################################################################################
    
    query = request.args.get('name')
    print ('------Search query:', query)

    if query:
        queryJson = requests.get(API_URL, params={'q': query}).json()

        # print('------Query Json:', queryJson)
        #return jsonify(queryJson)

        for anime in queryJson('data', []):
            anime_info = {
                'title': anime.get("title"),
                'image': anime.get("images", {}).get("jpg", {}).get("image_url"), 
                    #is jpg but there is webp
                'episodes': anime.get("episodes"),
                'duration': anime.get("duration")
                # 'trailer': anime.get(),
                'MALurl': anime.get(),
                'status': anime.get("status"),
                'year': anime.get("year")
                'genres': anime.get("genres", [])
                'demographics': anime.get 
            }
        
        print(anime_info)


    

# TODO watched-anime #################################################################################################################

# TODO just-finished #################################################################################################################

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5006)