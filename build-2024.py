
import sys
import os
import re
from pprint import pprint
from ics import Calendar, Event
import requests
from bs4 import BeautifulSoup

# initialize dist dir
dist = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'dist', '2024')
if not os.path.isdir(dist):
    os.mkdir(dist)
    # open(os.path.join(dist, '.gitkeep'), 'a').close()

# retrieve the BOE document
r = requests.get("https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-22014")

# store original document as a reference
with open(os.path.join(dist, '_boe.html'), 'wb') as fd:
    fd.write(r.content)

soup = BeautifulSoup(r.content, "html.parser")
table = soup.select_one(".tabla_girada_condensada")
# print(table.prettify())

# initialize 'Comunidaes Autonomas' and Calendar storage
cas = []
calendar = {}

for ca in table.find('thead').find_all('tr')[1].find_all('th'):
    # print(ca.text.strip())
    cas.append(re.sub(r' \(\d+\)', '', ca.text.strip()))
    calendar[cas[-1]] = []

# print(cas)

# fixed months as BOE representation
months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
          'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
current_month = None

# Iterate over rows and cols to guess each holiday for every CA
# We flip the table from holiday->CAs to CAs->holiday
for tr in table.find('tbody').find_all('tr'):
    first_col = tr.find('td').text.strip()

    if first_col in months:
        current_month = months.index(first_col) + 1
        continue
    # first row can be the month, or the holiday string
    holiday = first_col
    # print(current_month, holiday)

    # rest of the cells represents if a CA owns a holiday
    idx = -1
    for td in tr.find_all('td'):
        idx += 1

        if idx == 0:
            continue

        ca = cas[idx-1]
        day = int(re.sub(r'^(\d+).*', r'\1', holiday))

        if '*' in td.text.strip():
            calendar[ca].append((re.sub(r'^(\d+) ', '', holiday), f"2024-{current_month:02}-{day:02}"))

# pprint(calendar)
# for ca, holidays in calendar.items():
#      print(ca, len(holidays))

for ca, holidays in calendar.items():
    cal = Calendar()

    for holiday in holidays:
        ev = Event()

        ev.name = holiday[0]
        ev.begin = holiday[1]
        ev.make_all_day()
        cal.events.add(ev)

    with open(os.path.join(dist, f"{ca}.ics"), 'w') as ics_file:
        ics_file.writelines(cal.serialize_iter())
