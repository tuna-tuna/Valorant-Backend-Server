# Valorant Backend Server

## About

- This is the backend server which relays json responses obtained from api used by official valorant client.
- This server caches the response for 10 minutes to prevent from spamming the RSO Auth requests.



## Usage

- Clone this repo.
- Install the dependencies from Pipfile.
- Install the Redis (if you use Windows, then install Memurai instead) and run it on default port.
- Run ```uvicorn main:app```  (If you would like to enable hot reload function, run ```uvicorn main:app --reload```)  and now you can access to the api.



## Endpoints

### Match-making Rating(/mmr/player/{region}/{puuid})

- Get the match making rating for a player

### Match ID History(/match-history/{region}/{puuid})

- Note that these three endpoints get only match ids and the gamestart time etc...

- Get recent matches for player

- **Unrated(/match-history/unrated/{region}/{puuid})**
  - Get recent unrated matches for player

- **Competitive(/match-history/competitive/{region}/{puuid})**
  - Get recent competitive matches for player

### Match History with detailed match data

- **Unrated(/match-history/unrated-matches/{region}/{puuid})**
  - Get recent 5 unrated matches with detailed match data

- **Competitive(/match-history/competitive-matches/{region}/{puuid})**
  - Competitive version of the above endpoint

### Match Details(/match-details/{region}/{match_id})

- Get the detailed match data

### Leaderboard(/mmr/leaderboard/{region}/{leaderboardregion}/{season_id}/{size})

- Get the competitive leaderboard for a given season



## Thanks

- Big thanks to amazing works on github and resources on Valorant App Developers Discord.



## Legal

- Riot Games, VALORANT, and any associated logos are trademarks, service marks, and/or registered trademarks of Riot Games, Inc.
- This project is not affiliated, maintained, authorized sponsored or endorsed by Riot Games, Inc in any way.
- I don't have responsibilities for any legalities that may occur from using this project. Please use at your **own** risk.

