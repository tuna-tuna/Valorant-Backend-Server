import re
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
from collections import OrderedDict
import pickle #for saving ssid cookies

class Auth:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth_error = 'Unknown Error occurred.'
        self.clientVersion = None
        self.ssid_cookie = None

    def authenticate(self):
        try:
            class SSLAdapter(HTTPAdapter):
                def init_poolmanager(self, connections, maxsize, block=False):
                    self.poolmanager = PoolManager(num_pools=connections,
                                            maxsize=maxsize,
                                            block=block,
                                            ssl_version=ssl.PROTOCOL_TLSv1_2)
            data = {
                'client_id': 'play-valorant-web-prod',
                'nonce': '1',
                'redirect_uri': 'https://playvalorant.com/opt_in',
                'response_type': 'token id_token',
                'scope': 'account openid'
            }
            headers = OrderedDict({
                'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)'
            })
            session = requests.Session()
            session.mount('https://auth.riotgames.com/api/v1/authorization', SSLAdapter())
            session.headers = headers
            r = session.post('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)

            with session.get('https://valorant-api.com/v1/version') as r:
                r = r.json()
                self.clientVersion = r["data"]["riotClientVersion"]
            
            data = {
                'type': 'auth',
                'username': self.username,
                'password': self.password
            }
            with session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers) as r:
                data = r.json()
            if data['type'] == 'auth':
                self.auth_error = 'Username or password may be incorrect.'
            elif data['type'] == 'multifactor':
                twoFA = input('Input 2FA Code: ')
                data = {
                    "type": "multifactor",
                    "code": twoFA,
                    "rememberDevice": True
                }
                with session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers) as r:
                    self.ssid_cookie = 'ssid=' + r.cookies.get('ssid') + '; Path=/; HttpOnly; Secure; SameSite=None'
                    with open('cookie.pickle', 'wb') as f:
                        pickle.dump(self.ssid_cookie, f)
                    data = r.json()
            pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(data['response']['parameters']['uri'])[0] 
            access_token = data[0]

            headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Host': "entitlements.auth.riotgames.com",
                'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {access_token}',
            }
            with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
                data = r.json()
            entitlements_token = data['entitlements_token']
            headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Host': "auth.riotgames.com",
                'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {access_token}',
            }
            with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
                data = r.json()
            headers['X-Riot-Entitlements-JWT'] = entitlements_token
            headers['X-Riot-ClientVersion'] = self.clientVersion
            headers['X-Riot-ClientPlatform'] = 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
            del headers['Host']
            session.close()
            return headers
        except Exception as e:
            raise RuntimeError(self.auth_error)

    def tryReAuth(self):
        class SSLAdapter(HTTPAdapter):
                def init_poolmanager(self, connections, maxsize, block=False):
                    self.poolmanager = PoolManager(num_pools=connections,
                                            maxsize=maxsize,
                                            block=block,
                                            ssl_version=ssl.PROTOCOL_TLSv1_2)
        try:
            with open('cookie.pickle', 'rb') as f:
                self.ssid_cookie = pickle.load(f)
        except:
            raise
        session = requests.Session()
        with session.get('https://valorant-api.com/v1/version') as r:
                r = r.json()
                self.clientVersion = r["data"]["riotClientVersion"]
        data = {
            'client_id': "play-valorant-web-prod",
            'nonce': 1,
            'redirect_uri': "https://playvalorant.com/opt_in",
            'response_type': "token id_token",
            'scope': "account openid"
        }
        headers = {
            'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
            'Cookie': self.ssid_cookie
        }
        session.mount('https://auth.riotgames.com/api/v1/authorization', SSLAdapter())
        session.headers = headers
        r = session.post('https://auth.riotgames.com/api/v1/authorization', json = data, headers = headers)
        self.ssid_cookie = 'ssid=' + r.cookies.get('ssid') + '; Path=/; HttpOnly; Secure; SameSite=None'
        with open('cookie.pickle', 'wb') as f:
            pickle.dump(self.ssid_cookie, f)
        data = r.json()
        pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(data['response']['parameters']['uri'])[0]
        access_token = data[0]
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': "entitlements.auth.riotgames.com",
            'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {access_token}',
        }
        with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
            data = r.json()
        entitlements_token = data['entitlements_token']

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': "auth.riotgames.com",
            'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {access_token}',
        }

        with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
            data = r.json()
        headers['X-Riot-Entitlements-JWT'] = entitlements_token
        headers['X-Riot-ClientVersion'] = self.clientVersion
        headers['X-Riot-ClientPlatform'] = 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
        del headers['Host']
        session.close()
        return headers
        #Sometimes it fails with exception 'response'
        #But I haven't tried to resolve it cuz it's vary rare

    def tryAuth(self):
        headers = {}
        try:
            headers = self.tryReAuth()
        except Exception as e:
            headers = self.authenticate()
        return headers