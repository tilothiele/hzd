import requests

url = "http://hzd.chromosoft.de/login"

def fetch_session():
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Fehlerhafter Statuscode: {response.status_code}")
    cookies = response.cookies

    ci_session = cookies.get("ci_session")
    phpsessid = cookies.get("PHPSESSID")

    return ci_session, phpsessid

