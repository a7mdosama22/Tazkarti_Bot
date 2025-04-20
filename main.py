import time
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

CHECK_INTERVAL = 300  # وقت الانتظار بين كل محاولة فحص بالثواني

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
TEAM_NAME = os.environ["TEAM_NAME"]

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        print("✅ Message sent" if response.status_code == 200 else f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def check_match_loop():
    while True:
        print(f"🔍 Checking for '{TEAM_NAME}'...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://www.tazkarti.com/#/matches")
        time.sleep(5)

        match_found = False
        teams_elements = driver.find_elements(By.CLASS_NAME, "teams")
        for team_div in teams_elements:
            if TEAM_NAME.lower() in team_div.text.lower():
                print(f"[{datetime.now()}] ✅ Match for '{TEAM_NAME}' is available!")
                message = f"✅ Match for '{TEAM_NAME}' is now available on Tazkarti!"
                send_telegram_message(BOT_TOKEN, CHAT_ID, message)
                match_found = True
                break

        if not match_found:
            print(f"[{datetime.now()}] ❌ No match for '{TEAM_NAME}' yet.")

        driver.quit()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    check_match_loop()
