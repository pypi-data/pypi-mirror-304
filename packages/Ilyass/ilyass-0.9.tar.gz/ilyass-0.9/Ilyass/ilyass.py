# Ilyass/hotmail.py
import requests
import random
from random import randrange
import json
from concurrent.futures import ThreadPoolExecutor

class HotmailChecker:
    @staticmethod
    def HotmailEm(email):
        while True:
            try:
                res = requests.get('https://signup.live.com/signup')
                amsc = res.cookies.get_dict().get('amsc')
                canary = res.text.split('"apiCanary":"')[1].split('"')[0].encode().decode('unicode_escape')

                cookies = {'amsc': amsc}

                headers = {
                    'authority': 'signup.live.com',
                    'accept': 'application/json',
                    'canary': canary,
                    'origin': 'https://signup.live.com',
                    'referer': 'https://signup.live.com/signup?lic=1&uaid=f26d1e8726944e3f9cc96aafdfdf8225',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                }

                json_data = {
                    'clientExperiments': [
                        {
                            'parallax': 'enablejspublickeydeprecationexperiment',
                            'control': 'enablejspublickeydeprecationexperiment_control',
                            'treatments': ['enablejspublickeydeprecationexperiment_treatment'],
                        }
                    ]
                }

                response = requests.post(
                    'https://signup.live.com/API/EvaluateExperimentAssignments',
                    cookies=cookies,
                    headers=headers,
                    json=json_data
                ).json()

                canary = response['apiCanary']
                break

            except:
                pass

        cookies = {'amsc': amsc}
        headers = {
            'canary': canary,
            'origin': 'https://signup.live.com',
            'referer': 'https://signup.live.com/signup?lic=1&uaid=3daaf5bf6b70499d8a5035844d5bbfd8',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        json_data = {'signInName': email}

        response = requests.post(
            'https://signup.live.com/API/CheckAvailableSigninNames',
            cookies=cookies,
            headers=headers,
            json=json_data
        ).text

        return True if '"isAvailable":true' in response else False


class Instagram:
    @staticmethod
    def usergen(year):
        if year == 2011:
            id_range = 17699999
        elif year == 2012:
            id_range = 263014407
        elif year == 2013:
            id_range = 361365133
        elif year in range(2014, 2024):
            id_range = 61331927186
        else:
            return None

        def gg():
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                'x-ig-app-id': '936619743392459',
                'x-csrftoken': 'QOeFYsOi8enKuW80uC0WezhvEgiydc2Y',
                'x-ig-www-claim': 'hmac.AR3iNxyHufbREf9pIUL6m2ciMIIxA3vQTyCHW_yWjgu5dmsq',
            }

            data = {
                'av': '17841408545457742',
                '__user': '0',
                '__a': '1',
                '__req': '53',
                'dpr': '1',
                '__csr': 'iMkMF5NsIh2I4Aggpik9SLfZgxAZOsJh6DcNcUFXH-GHqnlaoSiypHBiVaFkhtdFmO',
                '__spin_r': '1014910249',
                'variables': '{"id":"' + str(randrange(10000, id_range)) + '","render_surface":"PROFILE"}',
                'server_timestamps': 'true',
                'doc_id': '7663723823674585',
            }

            try:
                response = requests.post(
                    'https://www.instagram.com/graphql/query',
                    headers=headers,
                    data=data
                )
                username = response.json()['data']['user']['username']
                return username

            except:
                return None

        