import requests


def login_to_chromosoft(ci_session, phpsessid, username, password):
    # Formulardaten (ersetze ggf. username/password)
    form_data = {
        username: username,
        password: password,
        'chromo-service-identifier': ''
    };

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        "Content-Type": "application/x-www-form-urlencoded",
        'Origin': 'https://hzd.chromosoft.de',
        'Referer': 'https://hzd.chromosoft.de/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    # Cookies setzen
    cookies = {
        "PHPSESSID": phpsessid,
        "ci_session": ci_session
    }

    response = requests.post('https://hzd.chromosoft.de/login', data=form_data, cookies=cookies, headers=headers);


    print("Antwort: ", response.text)
    print(response.status_code)
    print(response.headers)
