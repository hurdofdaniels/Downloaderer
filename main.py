import request, sys

getShows = request.getShows(sys.argv[1])
print(getShows[1][4])