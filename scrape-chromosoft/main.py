
from invoke00_create_session import fetch_session
from invoke01_login import login_to_chromosoft
from invoke02_search import search
import os
from dotenv import load_dotenv

try:
    ci_session, phpsessid = fetch_session()
    #print("ci_session:", ci_session)
    #print("PHSESSID:", phpsessid)
    login_to_chromosoft(ci_session=ci_session,
                        phpsessid=phpsessid,
                        username=os.getenv("USERNAME"),
                        password=os.getenv("PASSWORD"))
    print('nach login die suche...')
    search(ci_session=ci_session,
        phpsessid=phpsessid)

except Exception as e:
    print("Fehler:", e)