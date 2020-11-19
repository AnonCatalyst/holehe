from holehe.core import *
from holehe.localuseragent import *

def mail_ru(email):
    headers = {
        'authority': 'account.mail.ru',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://account.mail.ru',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://account.mail.ru/recovery?email={email}',
        'user-agent': random.choice(ua["browsers"]["chrome"]),
        'accept-language': 'ru',
    }

    data = 'email={email}&htmlencoded=false'.replace('@', '%40')

    response = requests.post(
        'https://account.mail.ru/api/v1/user/password/restore',
        headers=headers,
        data=data)

    if response.status_code == 200:
        try:
            reqd = response.json()
            if reqd['status'] == 200:
                phones = ', '.join(reqd['body'].get('phones', [])) or None
                emails = ', '.join(reqd['body'].get('emails', [])) or None
                return({"rateLimit": False, "exists": True, "emailrecovery": emails, "phoneNumber": phones, "others": None})
            else:
                # email not exists or some problem
                return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        except BaseException:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
