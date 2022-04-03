import requests
import aiohttp
import json
import sys
import os
import time
from debug import Debug

class Endpoints:
    def __init__(self):
        pass

    async def fetch(self, session: aiohttp.ClientSession, endpoint: str, region: str, headers: dict = {}, funcName: str = '', puuid: str = ''):
        fileName: str = funcName + '_' + puuid + '.json'
        filePath: str = './tmp/' + fileName
        url: str = 'https://pd.' + region + '.a.pvp.net/' + endpoint
        try:
            updateTime: float = os.path.getmtime(filePath)
            if time.time() - updateTime > 600:
                if Debug.debugFlag: print('Cache expired.')
                raise
            else:
                with open(filePath, 'r') as r:
                    if Debug.debugFlag: print('Cache found.')
                    data = json.load(r)
                    return data
        except:
            if Debug.debugFlag: print('Available cache not found.')
            async with session.get(url, headers = headers) as r:
                data = await r.json(content_type=None)
            with open(filePath, 'w') as r:
                json.dump(data, r, indent=4)
                if Debug.debugFlag: print('Cache generated.')
            return data

    async def mmr_FetchPlayer(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        endpoint: str = 'mmr/v1/players/' + puuid
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid=puuid)
        return data

    async def matchHistory(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        endpoint: str = 'match-history/v1/history/' + puuid
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid=puuid)
        return data

    async def unratedHistory(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        endpoint: str = 'match-history/v1/history/' + puuid + '?queue=unrated'
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid=puuid)
        return data

    async def competitiveHistory(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        endpoint: str = 'match-history/v1/history/' + puuid + '?queue=competitive'
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid=puuid)
        return data

    async def unratedMatches(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        matchHistory = await self.unratedHistory(session, region, puuid, headers)
        matchIDList = []
        matchDataList = []
        for i in range(5):
            matchID = matchHistory["History"][i]["MatchID"]
            matchIDList.append(matchID)
        for match in matchIDList:
            data = await self.matchDetails(session, region, match, headers)
            matchDataList.append(data)
        matchesData = {}
        matchesData["Matches"] = matchDataList
        matchesData["subject"] = puuid
        return matchesData

    async def competitiveMatches(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        matchHistory = await self.competitiveHistory(session, region, puuid, headers)
        matchIDList = []
        matchDataList = []
        for i in range(5):
            matchID = matchHistory["History"][i]["MatchID"]
            matchIDList.append(matchID)
        for match in matchIDList:
            data = await self.matchDetails(session, region, match, headers)
            matchDataList.append(data)
        matchesData = {}
        matchesData["Matches"] = matchDataList
        matchesData["subject"] = puuid
        return matchesData

    async def matchDetails(self, session: aiohttp.ClientSession, region: str, match_id: str, headers: dict):
        endpoint: str = 'match-details/v1/matches/' + match_id
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid=match_id)
        return data

    async def competitiveUpdates(self, session: aiohttp.ClientSession, region: str, puuid: str, headers: dict):
        endpoint: str = 'mmr/v1/players/' + puuid + '/competitiveupdates?queue=competitive'
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid=puuid)
        return data

    async def mmrLeaderboard(self, session: aiohttp.ClientSession, region: str, leaderboardRegion: str, seasonId: str, endIndex: str, headers: dict):
        endpoint: str = 'mmr/v1/leaderboards/affinity/' + leaderboardRegion + '/queue/competitive/season/' + seasonId + '?startIndex=0&size=' + endIndex
        funcName: str = sys._getframe().f_code.co_name
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers, funcName=funcName, puuid='leaderboard')
        return data

    #Just for testing a request
    def test(self, headers: dict):
        data = requests.get('https://example.com', headers = headers).json()
        return data