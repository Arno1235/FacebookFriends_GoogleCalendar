from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle
import csv

options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
# options.add_argument("--headless") # not possible because of manual login

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

driver.get("https://www.facebook.com")

input("Log in and press enter...")

driver.get("https://www.facebook.com/events/birthdays")

wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'x1gslohp.xw3qccf.x12nagc.xsgj6o6')))

# scroll all the way down
for scroll in range(20):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)

birthdays = []

for date in driver.find_elements(By.CLASS_NAME, 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1tu3fi.x676frb.x1pg5gke.xvq8zen.xo1l8bm.xi81zsa'):
    date = date.get_attribute("innerText")

    if date[-3:] == 'old':
        continue
    
    birthdays.append(["", date.split(',')[0]])

for i, name in enumerate(driver.find_elements(By.CLASS_NAME, 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xzsf02u')[-len(birthdays):]):
    name = name.get_attribute("innerText") + "'s Birthday"
    birthdays[i][0] = name

    print(f'found: {name} is {birthdays[i][1]}')

for person in driver.find_elements(By.CLASS_NAME, 'x1gslohp.xw3qccf.x12nagc.xsgj6o6'):

    actions.move_to_element(person).perform()

    tt_text = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xzsf02u.x1yc453h'))).text
    print(f'found: {tt_text}')

    birthdays.append(tt_text.split(' is '))

print(f'found {len(birthdays)} birthdays!')

with open("birthdays_checkpoint.p", "wb" ) as f:
	pickle.dump(birthdays, f)
     
# --- CHECKPOINT ---

with open("birthdays_checkpoint.p", "rb" ) as f:
    birthdays = pickle.load(f)

csv_list = [["Subject", "Start date", "All Day Event"]]

months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

for birthday in birthdays:
    csv_list.append([birthday[0], f'{birthday[1].split(" ")[1]}/{months_in_year.index(birthday[1].split(" ")[0]) + 1}/2023', "True"])

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_list)