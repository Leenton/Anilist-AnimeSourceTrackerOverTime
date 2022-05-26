import requests
import json

def getList(yeartosearch):

    #Get list of all the anime that aired in the time range the user specified

    animeForYear = []  

    def search(year, format):
        repeat = True
        x = 1
        while(repeat):
            query ='''
query ($page: Int, $perPage: Int ) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media(startDate_greater: ''' + str(year) + ''', startDate_lesser: ''' + str(year + 1) + ''', type: ANIME, format: '''+ format +''', countryOfOrigin: JP) {
      startDate {
        year
      }
      title {
        romaji
      }
      source
    }
  }
}'''
            variables = {
                'page': x
                }

            url = 'https://graphql.anilist.co'
            response = requests.post(url, json={'query': query, 'variables': variables})

            #Check if the loop has to be repeated to grab more items
            j = response.json()
            ans = bool(j['data']['Page']['pageInfo']['hasNextPage'])
            if(ans):
                repeat = True
                x = x + 1
            else:
                repeat = False

            for items in j['data']['Page']['media']:
                animeForYear.append(items['source'])
    
    #formatlist = ["TV","TV_SHORT","MOVIE","OVA","ONA"]
    formatlist = ["ONA"]
    for x in formatlist:
        search(yeartosearch, x)   

    
    return animeForYear

def parseData(animeForYearArray):
    
    sourceOriginal = 0
    sourceManga = 0
    sourceLightNovel = 0
    sourceVisualNovel = 0
    sourceVideoGame = 0
    sourceOther = 0
    sourceNovel = 0
    sourceNone = 0

    for x in range(len(animeForYearArray) -1):
        if animeForYearArray[x] == "ORIGINAL":
            sourceOriginal = sourceOriginal + 1
        elif animeForYearArray[x] == "MANGA":
            sourceManga = sourceManga + 1
        elif animeForYearArray[x] == "LIGHT_NOVEL":
            sourceLightNovel = sourceLightNovel + 1
        elif animeForYearArray[x] == "VISUAL_NOVEL":
            sourceVisualNovel = sourceVisualNovel + 1
        elif animeForYearArray[x] == "VIDEO_GAME":
            sourceVideoGame = sourceVideoGame + 1
        elif animeForYearArray[x] == "OTHER":
            sourceOther = sourceOther + 1
        elif animeForYearArray[x] == "NOVEL":
            sourceNovel = sourceNovel + 1
        else:
            sourceNone = sourceNone + 1

    print("Original = " + str(sourceOriginal))
    print("Manga = " + str(sourceManga))
    print("Light Novel = " + str(sourceLightNovel))
    print("Visual Novel = " + str(sourceVisualNovel))
    print("Video Game = " + str(sourceVideoGame))
    print("Other = " + str(sourceOther))
    print("Novel = " + str(sourceNovel))
    print("Null = " + str(sourceNone))
    print("Total Anime = " + str(len(animeForYearArray)))
    

start = int(input("Please input an interger for the year you want to start collecting data from: "))
while(start < 2021):
    print("\nThe following is the distribution of anime adaptation sources from the following year " + str(start) + "\n")
    parseData(getList(start))
    start = start + 1

