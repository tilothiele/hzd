import re
from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def ntfy(channel, message, sign):
    # Ziel-URL
    url = f"https://ntfy.emsgmbh-tt-homeoffice.srv64.de/{channel}"

    # Nachricht (du kannst auch f-Strings nutzen, wenn du eine Variable wie count einsetzen willst)
#    count = 3
#    message = f"ems-gitlab Backup Abbruch: Es laufen bereits {count} rsync-Prozesse."

    # Header definieren (wie bei curl: -H "X-Tags: stop_sign")

    headers = {
        "X-Tags": sign
    }

    # POST-Request absenden
    response = requests.post(url, data=message.encode("utf-8"), headers=headers)


username = os.getenv("CHROMOSOFT_USERNAME")
password = os.getenv("CHROMOSOFT_PASSWORD")

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://hzd.chromosoft.com/login")
    page.locator("input[name=\"username\"]").click()
    page.locator("input[name=\"username\"]").fill(username)
    page.locator("input[name=\"username\"]").press("Tab")
    page.locator("input[name=\"password\"]").fill(password)
    page.get_by_role("button", name="anmelden").click()
    page.get_by_role("listitem").filter(has_text="Suche").click()
    page.get_by_role("link", name="nach Personen").click()
    page.get_by_role("link", name="Powersuche").click()
    page.get_by_text("Person", exact=True).click()
    page.get_by_role("row", name="Region").get_by_role("textbox").click()
    page.locator("span").filter(has_text=re.compile(r"^Nord$")).click()
    page.get_by_role("radio").first.check()
    page.locator(".ch_fld_cont_hldr > img").click()
    page.locator("input[name=\"chk_all_sel_reslts\"]").check()
    with page.expect_download() as download_info:
        page.get_by_role("img", name="speichere ausgewählte als").nth(1).click()
    download = download_info.value

    # vom Server vorgeschlagener Name
    filename = download.suggested_filename

    download.save_as(f"./{filename}")
    print(f"Datei gespeichert unter: {filename}")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
    ntfy("hzd", "chromosoft Mitglieder abgeglichen", "ok")
