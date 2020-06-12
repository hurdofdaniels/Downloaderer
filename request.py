import requests, json
from json import loads

JSON = open("secret.json", "r")

SECRET = json.load(JSON)

API_KEY = SECRET["API_KEY"]

def getShows(QUERY):
    URL_ID = 'https://api.themoviedb.org/3/search/multi?api_key={}&language=en-US&query={}'.format(API_KEY, QUERY)
    r = requests.get(url = URL_ID)
    results = r.json()['results']
    cachedData = []
    for result in results:
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

            data = []

            data.append(show_name)
            data.append(seasons)
            data.append(episodes)
            data.append(genre_list)
            data.append("https://image.tmdb.org/t/p/original{}".format(json["poster_path"]))

            cachedData.append(data)
            
        elif str(vidType) == "movie":
            URL = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(vidId, API_KEY)
            response = requests.get(url = URL)
            json = response.json()

    return cachedData

def getTorrents(QUERY):
    URL = 'http://sg.media-imdb.com/suggests/{}/{}.json'.format(QUERY[0].lower(), QUERY.lower())
    r = requests.get(URL)

    start = r.text.find("(")
    end = r.text.find(")")

    data = loads(r.text[start + 1:end])["d"][0]["id"]

    URL = 'https://eztv.io/api/get-torrents?imdb_id={}'.format(data)
    r = requests.get(url = URL)
    data = r.json()

    return data["torrents"]