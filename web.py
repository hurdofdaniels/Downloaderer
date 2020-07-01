import sys, asyncio
from request import getShows, getShowInfo, downloadShow
from flask import Flask, request, render_template, Markup
app = Flask(__name__)

@app.route('/')
def index():
  return render_template("main.html", pageTitle="Home")

@app.route("/shows/", methods=['GET', 'POST'])
def results():
  if request.method == 'POST':
    name = request.form.get('name').title()
    shows = getShows(name)
    
    showsHTML = ""

    for show in shows:
      if show[1] != 0 and show[2] != 0:
        showsHTML += '''<div class="panel" onclick="location.href='/shows/{showID}-{type}'">
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

@app.route('/shows/<pageID>-<pageType>', methods=['GET', 'POST'])
def resultsInfo(pageID, pageType):
  if request.method == 'GET':
    data = getShowInfo(pageType, pageID)
    
    rawHTML = ""

    for info in data:
      rawHTML += '''<div class="panel"">
          <div class="well">
              <h1>{Name}</h1>
              <div class="overlay-container">
                <img src="{Poster}" alt="{Description}" id="picture" onload="imgSize(this);">
                <div class="overlay">
                  <p>{Description}</p>
                  <form action="" method="POST"><input type="hidden" name="url" value="{DownloadUrl}"/><button type="submit" class="btn btn-primary">Download</button></form>
                </div>
              </div>
          </div>
      </div>'''.format(Name=info[1], Description=info[2], Poster=info[3], DownloadUrl=info[0])
    return render_template('downloads.html', pageTitle="Downloads", downloadContent=Markup(rawHTML))
  elif request.method == 'POST':
    downloadList = []
    downloadList.append(request.form.get('url'))
    print(downloadList)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(downloadShow(downloadList))
    loop.close()
    return request.form.get('url')


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
  app.run(host='0.0.0.0', port=8080, debug=True)