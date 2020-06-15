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

    for show in shows:
      if show[1] != 0 and show[2] != 0:
        showsHTML += '''<div class="panel" onclick="location.href='/results/{showID}-{type}'">
        <h1>{showTitle}</h1>
        <div class="overlay-container">
          <img src="{imgURL}" alt="{showTitle}" id="picture" onload="imgSize(this);">
          <div class="overlay">
            <p>Seasons: {seasons}, Episodes: {episodes}{genreName} {genre}</p>
          </div>
        </div>
      </div>'''.format(showTitle=show[0], showID=show[5], type=show[6], imgURL=show[4], seasons=show[1], episodes=show[2], genre=", ".join(show[3]), genreName=", Genres:" if len(show[3]) > 1 else ", Genre:" if len(show[3]) == 1 else "")
         #
    return render_template("results.html", pageTitle=name, resultInfo=Markup(showsHTML))
    #return "NULL"
  elif request.method == 'GET':
    return '''<h1>Huh?</h1>
    <p>Something messed up, try again.</p>'''

@app.route('/results/<pageID>-<pageType>', methods=['GET', 'POST'])
def resultsInfo(pageID, pageType):
  data = getShowInfo(pageType, pageID)

  rawHTML = ""

  for info in data:
    rawHTML += '''<h1>{Name}</h1>
    <p>{Description}<p>
    <br>'''.format(Name=info[1], Description=info[2])
  
  return render_template('downloads.html', downloadContent=Markup(rawHTML))

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