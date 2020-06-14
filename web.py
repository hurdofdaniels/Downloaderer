import sys
from request import getShows, getShowInfo
from flask import Flask, request, render_template, Markup
app = Flask(__name__)

@app.route('/')
def index():
  return render_template("main.html", pageTitle="Home")

@app.route("/results/", methods=['GET', 'POST'])
def results():
  if request.method == 'POST':
    name = request.form.get('name').title()
    shows = getShows(name)
    
    showsHTML = ""

    i = 0
    while i < len(shows):
      if shows[i][1] != 0 and shows[i][2] != 0:
        showsHTML += '''<div class="panel" onclick="location.href='/results/{showID}-{type}'">
        <h1>{showTitle}</h1>
        <div class="overlay-container">
          <img src="{imgURL}" alt="{showTitle}" id="picture" onload="imgSize(this);">
          <div class="overlay">
            <p>Seasons: {seasons}, Episodes: {episodes}{genreName} {genre}</p>
          </div>
        </div>
      </div>'''.format(showTitle=shows[i][0], showID=shows[i][5], type=shows[i][6], imgURL=shows[i][4], seasons=shows[i][1], episodes=shows[i][2], genre=", ".join(shows[i][3]), genreName=", Genres:" if len(shows[i][3]) > 1 else ", Genre:" if len(shows[i][3]) == 1 else "")
      i += 1
         #
    return render_template("results.html", pageTitle=name, resultInfo=Markup(showsHTML))
    #return "NULL"
  elif request.method == 'GET':
    return '''<h1>Huh?</h1>
    <p>Something messed up, try again.</p>'''

@app.route('/results/<pageID>-<pageType>', methods=['GET', 'POST'])
def resultsInfo(pageID, pageType):
  data = getShowInfo(pageType, pageID)

  return data

@app.route('/raw/', methods=['GET', 'POST'])
def raw():
  if request.method == 'POST':  #this block is only entered when the form is submitted
    name = request.form.get('name')
    shows = getShows(name)

    return str(shows)
  elif request.method == 'GET':
    return '''<h1>Huh?</h1>
    <p>Something messed up, try again.</p>'''

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)