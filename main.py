import os
import time
import json
import requests
from bs4 import BeautifulSoup
from login import email_addr, email_pwd
import notify

# TODO:
#     - (feat)Implement mongo or remote gist backend instead of local file
#     - (feat)Add text functionality through spark or vodafone gateway
#     - (docs)readme, comments and cleanup

endpoint = 'https://www.spca.nz/adopt?species=dogs&centres=all&breed=all&size=all&animal_id=&gender=male&minAge=0&maxAge=1&pageNum=1'
db_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'db.json')


recipients = [
    # 'yohan.temp.dev@gmail.com',
    # 'deroseclan@gmail.com',
    'yohanderose@gmail.com',
]

current_db = json.loads(
    open(db_path, 'r').read())
new_db = {}

log_str = ''
with open('/tmp/puppies.log', 'a+') as f:
    res = requests.get(endpoint)
    if res.status_code == 200:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '\n')

        soup = BeautifulSoup(res.text, 'html.parser')
        for card in soup.find_all('a', {'class': 'card-link--adopt'}, href=True):
            try:
                name = card.find('h3').text
                link = 'https://www.spca.nz' + card['href']
                img = 'https://www.spca.nz' + card.find(
                    'figure', {'class': 'card-image'}).find('img')['data-src']

                breed, age, location = [
                    field.text for field in card.find_all('h4')]

                key = name + ',' + location

                if new_db.get(key) == None:
                    new_db[key] = {'breed': breed,
                                   'age': age, 'location': location, 'link': link, 'img': img}
                else:
                    log_str += f'ERROR: Database already contains puppy named {name} in {location}'
            except Exception as e:
                log_str += f'{e}\n'

        set1 = set(new_db)
        set2 = set(current_db)
        new = list(set1 - set2)
        gone = list(set2 - set1)
        msg = ''
        for puppy in gone:
            log_str += f'{puppy} has been adopted\n'
        for puppy in new:
            log_str += f'{puppy} has been added\n'
            obj = new_db[puppy]
            name = puppy.split(',')[0]
            summary = f'{name} is a {obj["age"]} {obj["breed"]} in {obj["location"]}\n'
            link = f'Link: {obj["link"]}\n'
            msg += f'<p>{summary}</p>\n<p>{link}</p>\n<img src="{obj["img"]}">\n'

        if len(new) > 0:
            for recipient in recipients:
                notify.send_msg(recipient, msg, 'New SPCA Puppies',
                                {'email': email_addr, 'password': email_pwd},  'smtp.yandex.com')

        json.dump(new_db, open(db_path, 'w'))
        f.write(log_str + '\n')
    else:
        f.write(f'ERROR: {res.status_code}' + '\n')
    print(log_str)
    f.write('---' + '\n')
