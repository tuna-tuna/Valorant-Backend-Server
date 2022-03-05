import aiohttp
import aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from fastapi import FastAPI
import aiohttp
from authreq import Auth
from endpoints import Endpoints

app = FastAPI()
session = aiohttp.ClientSession()

@app.on_event('startup')
async def startup():
    redis = aioredis.from_url('redis://localhost', encoding = 'utf8', decode_responses = True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.on_event('shutdown')
async def shutdown():
    await session.close()

@cache()
async def get_cache():
    return 1

username = 'username here'
password = 'password here'
auth = Auth(username=username, password=password)
endpoints = Endpoints()

#--------------------------Endpoints-----------------------------
@app.get('/mmr/player/{region}/{puuid}')
@cache(expire=600)
async def getMMRPlayer(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.mmr_FetchPlayer(session, region, puuid, headers)
    return data

@app.get('/match-history/{region}/{puuid}')
@cache(expire=600)
async def getMatchHistory(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.matchHistory(session, region, puuid, headers)
    return data

@app.get('/match-history/unrated/{region}/{puuid}')
@cache(expire=600)
async def getUnratedHistory(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.unratedHistory(session, region, puuid, headers)
    return data

@app.get('/match-history/competitive/{region}/{puuid}')
@cache(expire=600)
async def getCompetitiveHistory(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.competitiveHistory(session, region, puuid, headers)
    return data

@app.get('/match-history/unrated-matches/{region}/{puuid}')
@cache(expire=600)
async def getUnratedMatches(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.unratedMatches(session, region, puuid, headers)
    return data

@app.get('/match-history/competitive-matches/{region}/{puuid}')
@cache(expire=600)
async def getCompetitiveMatches(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.competitiveMatches(session, region, puuid, headers)
    return data

@app.get('/match-details/{region}/{match_id}')
@cache(expire=600)
async def getMatchDetails(region: str, match_id: str):
    headers = auth.tryAuth()
    data = await endpoints.matchDetails(session, region, match_id, headers)
    return data

@app.get('/mmr/competitive/{region}/{puuid}')
@cache(expire=600)
async def getCompetitiveUpdates(region: str, puuid: str):
    headers = auth.tryAuth()
    data = await endpoints.competitiveUpdates(session, region, puuid, headers)
    return data

@app.get('/mmr/leaderboard/{region}/{leaderboardregion}/{season_id}/{size}')
@cache(expire=600)
async def getLeaderboard(region: str, leaderboardregion: str, season_id: str, size: str):
    headers = auth.tryAuth()
    data = await endpoints.mmrLeaderboard(session, region, leaderboardregion, season_id, size, headers)
    return data

#Just for testing specific url request
@app.get('/test')
async def test():
    headers = auth.tryAuth()
    data = endpoints.test(headers)
    return data