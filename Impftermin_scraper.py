from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import smtplib

TODAY = datetime.datetime.today().strftime ('%d.%m.%Y')
TIME_NOW = datetime.datetime.today().strftime("%H:%M")
MAIL_EMAIL = "censored"
MAIL_PASSWORD = "censored"
EMAIL = "censored"
PW = "censored!"
KEIN_TERMIN_NACHRICHT = f"Leider sind derzeit keine weiteren Termine ab dem {TODAY} verfügbar. Bitte ändern Sie Ihre Eingaben oder melden Sie sich in ein paar Tagen wieder und prüfen ob neue Termine verfügbar sind."

while True:
    #Website öffnen und Browser im Hintergrund laufen lassen
    chrome_driver_path = "/Users/peter/chromedriver"

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=option)
    driver.get("https://ciam.impfzentren.bayern/auth/realms/C19V-Citizen/protocol/openid-connect/auth?client_id=c19v-frontend&redirect_uri=https%3A%2F%2Fimpfzentren.bayern%2Fcitizen%2F&state=73627193-7650-4044-8710-5d53cccc1581&response_mode=fragment&response_type=code&scope=openid&nonce=1c49f45a-0e99-4a33-80f7-4610a205e50c")


    #Anmelde Formular ausfullen
    username = driver.find_element_by_name("username")
    username.send_keys(EMAIL)

    password = driver.find_element_by_name("password")
    password.send_keys(PW)
    password.send_keys(Keys.ENTER)


    #Person auswaehlen
    driver.get("https://impfzentren.bayern/citizen/overview/2D8C70C0-82DE-42EE-BF35-318B557D6E4A")


    #Termine öffnen
    driver.get("https://impfzentren.bayern/citizen/appointment-selection/2D8C70C0-82DE-42EE-BF35-318B557D6E4A")


    #Nächstmöglichen Termin finden
    time.sleep(4)
    starting_point = driver.find_element_by_name("possibleSiteId")
    starting_point.send_keys(Keys.TAB)

    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB)
    actions.perform()
    actions.perform()
    actions.perform()

    actions.send_keys(Keys.ENTER)
    actions.perform()

    #Ergebnisse auslesen
    time.sleep(2)
    try:
        infomessage = driver.find_element_by_xpath('//*[@id="main"]/div/div/form/div/div[3]/span/span')
        infomessage_text = infomessage.text
    except Exception:
        infomessage_text = ""


    #Mail Schicken
    if infomessage_text != KEIN_TERMIN_NACHRICHT:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MAIL_EMAIL, password=MAIL_PASSWORD)
            connection.sendmail(
                from_addr=MAIL_EMAIL,
                to_addrs=["robert@schoeberls.eu", "michael@schoeberls.eu"],
                msg=f"Subject: IMPFTERMIN IST JETZT DA\n\n"
                    f"Log dich jetzt schnell auf der Impf-Website an, es sollte nun ein Termin da sein! \n\n"
                    f"Klick den Link: https://impfzentren.bayern/citizen/")
            print(f"Termin Verfügbar \n{TIME_NOW} \n \n \n")
    else:
        print(f"Kein Termin \n{TIME_NOW} \n \n \n")

    driver.quit()
    time.sleep(600)




