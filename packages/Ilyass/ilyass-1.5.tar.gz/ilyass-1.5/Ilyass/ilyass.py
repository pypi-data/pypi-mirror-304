# Ilyass/hotmail.py
import requests
import random
from random import randrange
import json
from concurrent.futures import ThreadPoolExecutor
import hashlib
import uuid
from user_agent import generate_user_agent
from requests import post as post_request
from user_agent import generate_user_agent as generate_user_agent
from random import choice as random_choice
from random import randrange as random_range
import re
import os

ua = generate_user_agent()
dev = 'android-'
device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
uui = str(uuid.uuid4())

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

        return gg()

    @staticmethod
    def check(email):
        while True:
            try:
                session = requests.Session()
                session.headers.update({'User-Agent': ua})
                response = session.get('https://www.instagram.com/')
                csrf_token = session.cookies.get_dict().get('csrftoken')
                break
            except:
                continue

        headers = {
            'User-Agent': ua,
            'Cookie': f'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken={csrf_token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        data = {
            'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' + json.dumps({
                '_csrftoken': csrf_token,
                'adid': uui,
                'guid': uui,
                'device_id': device_id,
                'query': email
            }),
            'ig_sig_key_version': '4',
        }

        response = session.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).text
        if email in response:
            return True
        else:
            return False

    @staticmethod
    def rest(user):
        try:
            headers = {
                'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
                'X-Pigeon-Rawclienttime': '1700251574.982',
                'X-IG-Connection-Speed': '-1kbps',
                'X-IG-Bandwidth-Speed-KBPS': '-1.000',
                'X-IG-Bandwidth-TotalBytes-B': '0',
                'X-IG-Bandwidth-TotalTime-MS': '0',
                'X-Bloks-Version-Id': 'c80c5fb30dfae9e273e4009f03b18280bb343b0862d663f31a3c63f13a9f31c0',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-App-ID': '567067343352427',
                'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
                'Accept-Language': 'en-GB, en-US',
                'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'Connection': 'keep-alive',
                'Content-Length': '356',
            }
            data = {
                'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"' + user + '"}',
                'ig_sig_key_version': '4',
            }
            response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).json()
            r = response['email']
        except:
            r = ' Bad '
        return r

    @staticmethod
    def information(username):
        try:
            info = requests.get('https://anonyig.com/api/ig/userInfoByUsername/' + username).json()
        except:
            info = False
        try:
            Id = info['result']['user']['pk_id']
        except:
            Id = None

        try:
            followers = info['result']['user']['follower_count']
        except:
            followers = None
        try:
            following = info['result']['user']['following_count']
        except:
            following = None
        try:
            post = info['result']['user']['media_count']
        except:
            post = None
        try:
            name = info['result']['user']['full_name']
        except:
            name = None
        try:
            is_verified = info['result']['user']["is_verified"]
        except:
            is_verified = None
        try:
            is_private = info['result']['user']['is_private']
        except:
            is_private = None
        try:
            biography = info['result']['user']['biography']
        except:
            biography = None
        
        try:
            Id = int(Id)
            if 1 < Id <= 1278889:
                date = 2010
            elif 1279000 <= Id <= 17750000:
                date = 2011
            elif 17750001 <= Id <= 279760000:
                date = 2012
            elif 279760001 <= Id <= 900990000:
                date = 2013
            elif 900990001 <= Id <= 1629010000:
                date = 2014
            elif 1629010001 <= Id <= 2369359761:
                date = 2015
            elif 2369359762 <= Id <= 4239516754:
                date = 2016
            elif 4239516755 <= Id <= 6345108209:
                date = 2017
            elif 6345108210 <= Id <= 10016232395:
                date = 2018
            elif 10016232396 <= Id <= 27238602159:
                date = 2019
            elif 27238602160 <= Id <= 43464475395:
                date = 2020
            elif 43464475396 <= Id <= 50289297647:
                date = 2021
            elif 50289297648 <= Id <= 57464707082:
                date = 2022
            elif 57464707083 <= Id <= 63313426938:
                date = 2023
            else:
                date = 2024
        except:
            return None

        return {
            "name": name,
            "username": username,
            "followers": followers,
            "following": following,
            "date": date,
            "id": Id,
            "post": post,
            "bio": biography,
            "is_verified": is_verified,
            'is_private': is_private,
        }

characters = 'azertyuiopmlkjhgfdsqwxcvbn'
ids = []

class GmailChecker:
    @staticmethod
    def generate_token_and_host():
        try:
            
            random_name_part1 = ''.join(random_choice(characters) for _ in range(random_range(6, 9)))
            random_name_part2 = ''.join(random_choice(characters) for _ in range(random_range(3, 9)))
            random_host = ''.join(random_choice(characters) for _ in range(random_range(15, 30)))
            
            headers_for_initial_request = {
                "accept": "*/*",
                "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
                "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "google-accounts-xsrf": "1",
                "sec-ch-ua": "\"Not)A;Brand\";v=\"24\", \"Chromium\";v=\"116\"",
                "sec-ch-ua-arch": "\"\"",
                "sec-ch-ua-bitness": "\"\"",
                "sec-ch-ua-full-version": "\"116.0.5845.72\"",
                "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"24.0.0.0\", \"Chromium\";v=\"116.0.5845.72\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-model": "\"ANY-LX2\"",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-ch-ua-platform-version": "\"13.0.0\"",
                "sec-ch-ua-wow64": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-chrome-connected": "source=Chrome,eligible_for_consistency=true",
                "x-client-data": "CJjbygE=",
                "x-same-domain": "1",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                'user-agent': str(generate_user_agent()),
            }
            
            response_initial = requests.get(
                'https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB',
                headers=headers_for_initial_request
            )
            
            token = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', response_initial.text).group(2)
            cookies_initial = {
                '__Host-GAPS': random_host
            }
            
            headers_for_token_request = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'origin': 'https://accounts.google.com',
                'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
                'user-agent': generate_user_agent(),
            }
            
            data_for_token_request = {
                'f.req': f'["{token}","{random_name_part1}","{random_name_part2}","{random_name_part1}","{random_name_part2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
            }
            
            response_token = post_request(
                'https://accounts.google.com/_/signup/validatepersonaldetails',
                cookies=cookies_initial,
                headers=headers_for_token_request,
                data=data_for_token_request,
            )
            
            token_extracted = str(response_token.text).split('",null,"')[1].split('"')[0]
            host_extracted = response_token.cookies.get_dict()['__Host-GAPS']
            
            try:
                os.remove('tl.txt')
            except:
                pass
            with open('tl.txt', 'a') as file:
                file.write(f"{token_extracted}//{host_extracted}\n")
        
        except Exception as error:
            print(error)
            GmailChecker.generate_token_and_host()
    
    @staticmethod
    def gmail(email):
        if '@' in email:
            email = str(email).split('@')[0]
        
        try:
            try:
                file_content = open('tl.txt', 'r').read().splitlines()[0]
            except:
                GmailChecker.generate_token_and_host()
                file_content = open('tl.txt', 'r').read().splitlines()[0]
            
            token, host = file_content.split('//')
            cookies_for_check = {
                '__Host-GAPS': host
            }
            headers_for_check = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'origin': 'https://accounts.google.com',
                'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL={token}',
                'user-agent': generate_user_agent(),
            }
            
            params_for_check = {
                'TL': token,
            }
            
            data_for_check = (
                f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn&f.req=%5B%22TL%3A{token}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
                '&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D&gmscoreversion=undefined&flowName=GlifWebSignIn&'
            )
            
            response_check = post_request(
                'https://accounts.google.com/_/signup/usernameavailability',
                params=params_for_check,
                cookies=cookies_for_check,
                headers=headers_for_check,
                data=data_for_check,
            )
            
            if '"gf.uar",1' in str(response_check.text):
                return True
            elif '"er",null,null,null,null,400' in str(response_check.text):
                GmailChecker.generate_token_and_host()
                return GmailChecker.check_gmail(email)
            else:
                return False
        
        except:
            return GmailChecker.check_gmail(email)
