import requests
import aiohttp

class Endpoints:
    def __init__(self):
        pass

    async def fetch(self, session: aiohttp.ClientSession, endpoint: str, region: str, headers = {}):
        url = 'https://pd.' + region + '.a.pvp.net/' + endpoint
        async with session.get(url, headers = headers) as r:
            data = await r.json(content_type=None)
        return data

    async def mmr_FetchPlayer(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
        endpoint = 'mmr/v1/players/' + puuid
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    async def matchHistory(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
        endpoint = 'match-history/v1/history/' + puuid
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    async def unratedHistory(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
        endpoint = 'match-history/v1/history/' + puuid + '?queue=unrated'
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    async def competitiveHistory(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
        endpoint = 'match-history/v1/history/' + puuid + '?queue=competitive'
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    async def unratedMatches(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
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

    async def competitiveMatches(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
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

    async def matchDetails(self, session: aiohttp.ClientSession, region: str, match_id: str, headers):
        endpoint = 'match-details/v1/matches/' + match_id
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    async def competitiveUpdates(self, session: aiohttp.ClientSession, region: str, puuid: str, headers):
        endpoint = 'mmr/v1/players/' + puuid + '/competitiveupdates?queue=competitive'
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    async def mmrLeaderboard(self, session: aiohttp.ClientSession, region: str, leaderboardRegion: str, seasonId: str, endIndex: str, headers):
        endpoint = 'mmr/v1/leaderboards/affinity/' + leaderboardRegion + '/queue/competitive/season/' + seasonId + '?startIndex=0&size=' + endIndex
        data = await self.fetch(session, endpoint=endpoint, region=region, headers=headers)
        return data

    #Just for testing a request
    def test(self, headers):
        data = requests.get('https://example.com', headers = headers).json()
        return data