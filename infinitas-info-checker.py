import requests
import hashlib
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

website_url = "https://p.eagate.573.jp/game/infinitas/2/index.html"
hash_file = "hash.txt"

def calculate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def read_previous_hash():
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as file:
            return file.read().strip()
    else:
        return ''

def save_current_hash(hash_value):
    with open(hash_file, 'w') as file:
        file.write(hash_value)

def save_content(content):
    with open("content.html", 'w', encoding="utf-8") as file:
        file.write(content)

def check_for_update():
    response = requests.get(website_url)
    if response.status_code == 200:
        current_content = response.text
        info_main = BeautifulSoup(current_content, "html.parser").find(id="info-main")

        save_content(str(info_main))

        info1 = info_main.div

        ''' #To do - Shape the information into dictionary
        title = info1.strong
        date = info1.p
        latest_info = dict(title=title, date=date, body=)
        '''

        current_hash = calculate_hash(str(info_main))
        previous_hash = read_previous_hash()

        if current_hash != previous_hash:
            print("The information has been updated!")
            save_current_hash(current_hash)
            send_line_notify(str(info1))
        else:
            print("The information has not been updated.")

    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

def send_line_notify(message):
    load_dotenv()
    line_notify_api = 'https://notify-api.line.me/api/notify'
    line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': message}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    check_for_update()
    
