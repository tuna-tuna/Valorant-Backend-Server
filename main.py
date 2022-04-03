import aiohttp
import pickle
import time

from fastapi import FastAPI
import aiohttp
from authreq import Auth
from endpoints import Endpoints
from cache import Cache

app = FastAPI()
session = aiohttp.ClientSession()

@app.on_event('startup')
async def startup():
    print('Application Ready')

@app.on_event('shutdown')
async def shutdown():
    await session.close()

userdata = open('user.txt', 'r')
userdatalist = userdata.readlines()
username = userdatalist[0]
password = userdatalist[1]
auth = Auth(username=username, password=password)
endpoints = Endpoints()
cache = Cache()



#--------------------------Endpoints-----------------------------
@app.get('/mmr/player/{region}/{puuid}')
async def getMMRPlayer(region: str, puuid: str):
    fileName: str = 'getMMRPlayer_' + puuid
    headers: dict = auth.tryAuth()
    data = await endpoints.mmr_FetchPlayer(session, region, puuid, headers)
    return data

@app.get('/match-history/{region}/{puuid}')
async def getMatchHistory(region: str, puuid: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.matchHistory(session, region, puuid, headers)
    return data

@app.get('/match-history/unrated/{region}/{puuid}')
async def getUnratedHistory(region: str, puuid: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.unratedHistory(session, region, puuid, headers)
    return data

@app.get('/match-history/competitive/{region}/{puuid}')
async def getCompetitiveHistory(region: str, puuid: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.competitiveHistory(session, region, puuid, headers)
    return data

@app.get('/match-history/unrated-matches/{region}/{puuid}')
async def getUnratedMatches(region: str, puuid: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.unratedMatches(session, region, puuid, headers)
    return data

@app.get('/match-history/competitive-matches/{region}/{puuid}')
async def getCompetitiveMatches(region: str, puuid: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.competitiveMatches(session, region, puuid, headers)
    return data

@app.get('/match-details/{region}/{match_id}')
async def getMatchDetails(region: str, match_id: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.matchDetails(session, region, match_id, headers)
    return data

@app.get('/mmr/competitive/{region}/{puuid}')
async def getCompetitiveUpdates(region: str, puuid: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.competitiveUpdates(session, region, puuid, headers)
    return data

@app.get('/mmr/leaderboard/{region}/{leaderboardregion}/{season_id}/{size}')
async def getLeaderboard(region: str, leaderboardregion: str, season_id: str, size: str):
    headers: dict = auth.tryAuth()
    data = await endpoints.mmrLeaderboard(session, region, leaderboardregion, season_id, size, headers)
    return data

#--------------------Debug Endpoints-----------------------------
#Just for testing specific url request
@app.get('/test')
async def test():
    headers: dict = auth.tryAuth()
    data = endpoints.test(headers)
    return data

@app.get('/clearUnix')
async def clearUnix():
    auth.unixtime = 0.0
    return 'Unixtime cleared.'

@app.get('/showCookie')
async def showCookie():
    with open('cookie.pickle', 'rb') as f:
        cookie: str = pickle.load(f)
    return cookie