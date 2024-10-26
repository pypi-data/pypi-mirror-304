# Ilyass/hotmail.py
import requests


def check_availability(email):
    while True:
        try:

            res = requests.get('https://signup.live.com/signup')
            amsc = res.cookies.get_dict().get('amsc')
            canary = res.text.split('"apiCanary":"')[1].split('"')[0].encode().decode('unicode_escape')

            cookies = {
                'amsc': amsc,
            }

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
                        'treatments': [
                            'enablejspublickeydeprecationexperiment_treatment',
                        ],
                    },
                ],
            }

            response = requests.post(
                'https://signup.live.com/API/EvaluateExperimentAssignments',
                cookies=cookies,
                headers=headers,
                json=json_data,
            ).json()
            canary = response['apiCanary']
            break
        except:
            pass

    cookies = {
        'amsc': amsc,
    }

    headers = {
        'canary': canary,
        'origin': 'https://signup.live.com',
        'referer': 'https://signup.live.com/signup?lic=1&uaid=3daaf5bf6b70499d8a5035844d5bbfd8',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    json_data = {
        'signInName': email,
    }

    response = requests.post(
        'https://signup.live.com/API/CheckAvailableSigninNames',
        cookies=cookies,
        headers=headers,
        json=json_data,
    ).text

    if '"isAvailable":true' in response:
        return 'Available'
    else:
        return 'Not Available'
