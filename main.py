import time
import json
import requests
from bs4 import BeautifulSoup


endpoint = 'https://www.spca.nz/adopt?species=dogs&centres=all&breed=all&size=all&animal_id=&gender=male&minAge=0&maxAge=1&pageNum=1'

current_db = json.loads(open('./db.json', 'r').read())
new_db = {}

log_str = ''
with open('/tmp/puppies.log', 'a') as f:
    res = requests.get(endpoint)
    if res.status_code == 200:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '\n')

        soup = BeautifulSoup(res.text, 'html.parser')
        for card in soup.find_all('a', {'class': 'card-link--adopt'}):
            try:
                name = card.find('h3').text
                breed, age, location = [
                    field.text for field in card.find_all('h4')]

                key = name + ',' + location

                if new_db.get(key) == None:
                    new_db[key] = {'breed': breed,
                                   'age': age, 'location': location}
                else:
                    log_str += f'ERROR: Database already contains puppy named {name} in {location}'
            except Exception as e:
                log_str += f'{e}\n'

        set1 = set(new_db)
        set2 = set(current_db)
        new = list(set1 - set2)
        gone = list(set2 - set1)
        for puppy in gone:
            log_str += f'{puppy} has been adopted\n'
        for puppy in new:
            log_str += f'{puppy} has been added\n'

        # TODO: update db.json with new_db
        # json.dump(new_db, open('./db.json', 'w'))
        f.write(log_str + '\n')
    else:
        f.write(f'ERROR: {res.status_code}' + '\n')

    f.write('---' + '\n')
