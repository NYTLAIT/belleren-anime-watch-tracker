import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

API_URL = 'https://api.jikan.moe/v4/anime'
print(API_URL)


################################ NOTE ##################################
# return redirect(url_for('index')) #reloads the page
# 
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
        queryOutput = requests.get(API_URL, params={'q': query}).json()
        print('------Query output:', queryOutput)

    

# TODO watched-anime #################################################################################################################

# TODO just-finished #################################################################################################################

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5006)