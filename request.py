# Import all needed modules
from __future__ import unicode_literals
import requests, json, youtube_dl, re#, asyncio
from bs4 import BeautifulSoup

# Open the secret.json file
SECRET_FILE = open("secret.json", "r")

# Load it into the SECRET variable
SECRET = json.load(SECRET_FILE)

# Set API_KEY to API_KEY from SECRET
API_KEY = SECRET["API_KEY"]
# Set the DOWNLOAD_URL to DOWNLOAD_URL from SECRET
DOWNLOAD_URL = SECRET["DOWNLOAD_URL"]

# The inner web url for free shows
NON_PIRATE = ["10play"]
# The full url for free shows, The list index must match the NON_PIRATE list!
NON_PIRATE_URL = ["https://10play.com.au"]

def getShows(QUERY):
    URL_ID = 'https://api.themoviedb.org/3/search/multi?api_key={}&language=en-US&query={}'.format(API_KEY, QUERY)
    r = requests.get(url = URL_ID)
    returnedData = r.json()['results']
    cachedData = []
    for result in returnedData:
        vidId = result["id"]
        vidType = result["media_type"]
        if str(vidType) == "tv":
            URL = 'https://api.themoviedb.org/3/tv/{}?api_key={}&language=en-US'.format(vidId, API_KEY)
            response = requests.get(url = URL)
            json = response.json()

            genre_list = []

            for genre in json["genres"]:
                if json["genres"] != []:
                    genre_list.append(genre["name"])
                else:
                    genre_list = "NULL"

            show_name = json["name"]
            seasons = json["number_of_seasons"]
            episodes = json["number_of_episodes"]
            bg_path = "https://image.tmdb.org/t/p/original{}".format(json["poster_path"])
            if json["poster_path"] == None:
                bg_path = "https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png"
                
            show_id = json["id"]

            data = []

            data.append(show_name)
            data.append(seasons)
            data.append(episodes)
            data.append(genre_list)
            data.append(bg_path)
            data.append(show_id)
            data.append('tv')

            cachedData.append(data)
            
        elif str(vidType) == "movie":
            URL = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(vidId, API_KEY)
            response = requests.get(url = URL)
            json = response.json()

    return cachedData

def getShowInfo(QUERY_TYPE, QUERY_ID):
    URL = 'https://api.themoviedb.org/3/{}/{}?api_key={}&language=en-US'.format(QUERY_TYPE, QUERY_ID, API_KEY)
    response = requests.get(url = URL)
    jsonRes = response.json()
    htmlPage = jsonRes["homepage"]
    if htmlPage.split('://')[1].split(".")[0] in NON_PIRATE:
        print(htmlPage)
#        ydl_opts = {
#            'geo_bypass_country': 'au',
#            'quiet': True,
#            'outtmpl': 'DOWNLOADS/%(title)s - %(alt_title)s.%(ext)s'
#        }
#        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#            print("Downloading file")
#            ydl.download(["https://10play.com.au/masterchef/episodes/season-12/episode-1/tpv200411duoxs"])
#            print("Downloaded file")
        soup = BeautifulSoup(requests.get(htmlPage).text, 'html.parser')

        showData = soup.find('div', {'class', 'content__wrapper--inner'}).find_all('script')[1].string

        # When loading in JSON data with the loads function i get the error as follows, Fix it to make the program run!
        # AttributeError: 'dict' object has no attribute 'loads'
        javasciptData = json.loads(showData.split("const showPageData = ")[1].replace("};", "}")) #json.loads(showData.split("const showPageData = ")[1].replace("};", '}')) #loads(showData.split("const showPageData")[1].split(';')[0]) 
        
        extraData = javasciptData["subnavs"][0]["content"][0]["components"][0]["loadMoreUrl"]

        baseURL = NON_PIRATE_URL[NON_PIRATE.index(htmlPage.split('://')[1].split(".")[0])]
        
        fullURL = baseURL + extraData

        print(fullURL)

        resJsonShows = requests.get(url = fullURL).json()
        items = resJsonShows["items"]

        mainData = []

        reverse = False

        if "Ep. 1" not in items[0]:
            reverse = True

        for item in items:
            tmpData = []
            print(baseURL + item["cardLink"])

            tmpData.append(baseURL + item["cardLink"])

            tmpData.append(item["cardTitle"])

            tmpData.append(item["cardDescription"])

            tmpData.append(item["cardImage"]["retinaUrl"])

            mainData.append(tmpData)

        if reverse == True:
            mainData.reverse()

#        for info in soup.find('div', {'class', 'slick-list'}).find_all('a'):
#            if info != None:
#                tmpData = []
#
#                print(info['href'])
#
#                tmpData.append("https://10play.com.au{URL}".format(URL=info['href']))
#
#                print(info.find('h4', attrs={'class', 'card__title'}).string)
#
#                tmpData.append(info.find('h4', attrs={'class', 'card__title'}).string)
#
#                print(info.find('h5', attrs={'class', 'card__info'}).string)
#
#                tmpData.append(info.find('h5', attrs={'class', 'card__info'}).string)
#
#                mainData.append(tmpData)
#                info.decompose()
#        print(soup.find('div', {'class', 'slick-list'}).find_all('a'))
#        mainData.reverse()
    else:
        mainData = "Feature not yet added!"
    return mainData

async def downloadShow(QUERY):
        ydl_opts = {
            'geo_bypass_country': 'au',
            'quiet': True,
            'outtmpl': '{Download}%(title)s - %(alt_title)s.%(ext)s'.format(Download=DOWNLOAD_URL)
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading file")
            await ydl.download(QUERY)
            print("Downloaded file")

def getTorrents(QUERY):
    URL = 'http://sg.media-imdb.com/suggests/{}/{}.json'.format(QUERY[0].lower(), QUERY.lower())
    r = requests.get(URL)

    start = r.text.find("(")
    end = r.text.find(")")

    data = json.loads(r.text[start + 1:end])["d"][0]["id"]

    URL = 'https://eztv.io/api/get-torrents?imdb_id={}'.format(data)
    r = requests.get(url = URL)
    data = r.json()

    return data["torrents"]