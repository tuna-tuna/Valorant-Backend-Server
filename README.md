# Valorant Backend Server

[English Version is here](https://github.com/tuna-tuna/Valorant-Backend-Server/blob/master/README_EN.md)

## About

- Valorantのゲームクライアントで使用されているAPIにアクセスし、そのレスポンスをjson形式で提供するバックエンドサーバーです。
- RSO認証のスパムを防ぐため、レスポンスのデータを10分間キャッシュします。



## Usage

- リポジトリをクローンし、Pipfileを参考に必要なモジュールのインストール
- キャッシュのために使用するRedis(Windowsの場合はMemurai)をインストールし、デフォルトのポートで起動
- ```uvicorn main:app```(自動リロード機能を使用する場合```uvicorn main:app --reload```)を実行



## Endpoints

### Match-making Rating(/mmr/player/{region}/{puuid})

- シーズン別の各モードのスタッツなどを取得

### Match ID History(/match-history/{region}/{puuid})

- これら3つのエンドポイントはMatch ID及びゲームのスタート時間などの簡単な情報しか含みません

- 最近の数試合を取得

- **Unrated(/match-history/unrated/{region}/{puuid})**
  - 最近のアンレート数試合を取得

- **Competitive(/match-history/competitive/{region}/{puuid})**
  - 最近のコンペティティブ数試合を取得

### Match History with detailed match data

- **Unrated(/match-history/unrated-matches/{region}/{puuid})**
  - 最近のアンレート数試合を詳細な情報とともに取得

- **Competitive(/match-history/competitive-matches/{region}/{puuid})**
  - 最近のコンペティティブ数試合を詳細な情報とともに取得

### Match Details(/match-details/{region}/{match_id})

- 試合の詳細な情報を取得

### Leaderboard(/mmr/leaderboard/{region}/{leaderboardregion}/{season_id}/{size})

- 指定したシーズンのコンペティティブリーダーボードを取得



## Thanks

- Big thanks to amazing works on github and resources on Valorant App Developers Discord.



## Legal

- Riot Games, VALORANT, and any associated logos are trademarks, service marks, and/or registered trademarks of Riot Games, Inc.
- This project is not affiliated, maintained, authorized sponsored or endorsed by Riot Games, Inc in any way.
- I don't have responsibilities for any legalities that may occur from using this project. Please use at your **own** risk.