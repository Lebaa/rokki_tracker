from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import sqlite3
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
import datetime
import string
import MySQLdb as mysql
import sshtunnel


sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


def novar_db_command(command):
    with sshtunnel.SSHTunnelForwarder(
        ("ssh.eu.pythonanywhere.com"),
        ssh_username="Leba",
        ssh_password="Lebalol123",
        remote_bind_address=("Leba.mysql.eu.pythonanywhere-services.com", 3306),
    ) as tunnel:
        connection = mysql.connect(
            user="Leba",
            password="superpassu",
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            database="Leba$Kukko",
        )

        cur = connection.cursor()
        cur.execute(command)
        try:
            result = cur.fetchall()
        except:
            result = "vituiks män"

        connection.close()
        return result


def db_command(command, variables):
    with sshtunnel.SSHTunnelForwarder(
        ("ssh.eu.pythonanywhere.com"),
        ssh_username="Leba",
        ssh_password="Lebalol123",
        remote_bind_address=("Leba.mysql.eu.pythonanywhere-services.com", 3306),
    ) as tunnel:
        connection = mysql.connect(
            user="Leba",
            password="superpassu",
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            database="Leba$Kukko",
        )

        cur = connection.cursor()
        cur.execute(command, variables)
        result = cur.fetchall()
        connection.commit()
        connection.close()
        return result


clean = lambda dirty: "".join(filter(string.printable.__contains__, dirty))


def find_element(driver, xpath):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element


def ei_kkaupassa(driver, xpath):
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element


def ei_skaupassa(driver, xpath):
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, xpath,))
    )
    return element


def find_ruksi(driver, xpath):
    element = WebDriverWait(driver, 30).until(
        (EC.element_to_be_clickable((By.XPATH, xpath)))
    )
    return element


def create_kauppa():
    command = "CREATE TABLE IF NOT EXISTS kauppa ( id INT AUTO_INCREMENT PRIMARY KEY, nimi TEXT, ketju TEXT)"
    novar_db_command(command)


def create_tuote():
    command = "CREATE TABLE IF NOT EXISTS tuote (id INT AUTO_INCREMENT PRIMARY KEY, nimi TEXT, yksiköt TEXT, viivakoodi TEXT)"
    novar_db_command(command)


def create_hintaKaupassa():
    command = "CREATE TABLE IF NOT EXISTS hintaKaupassa ( id INT AUTO_INCREMENT PRIMARY KEY, tuote_id INTEGER, kauppa_id INTEGER, hinta DECIMAL(4,2), paivays TEXT, FOREIGN KEY(tuote_id) REFERENCES tuote(id), FOREIGN KEY(kauppa_id) REFERENCES kauppa(id))"
    novar_db_command(command)


def create_hinta_historia():
    command = "CREATE TABLE IF NOT EXISTS hintaHistoria (id INT AUTO_INCREMENT PRIMARY KEY, tuote_id INTEGER, kauppa_id INTEGER, hinta TEXT, alkupvm TEXT, FOREIGN KEY(tuote_id) REFERENCES tuote(id), FOREIGN KEY(kauppa_id) REFERENCES kauppa(id))"
    novar_db_command(command)


def insert_tuote(nimi, nro, viivakoodi):
    sql = "INSERT INTO tuote (nimi, yksiköt, viivakoodi) VALUES (%s,%s,%s)"
    db_command(sql, (nimi, nro, viivakoodi))


def insert_kaupat(kauppa, ketju):
    command = "INSERT INTO kauppa (nimi, ketju) VALUES (%s, %s)"
    db_command(command, (kauppa, ketju))


def hinta_tauluun(tuote_id, kauppa_id, hinta, date, kappalehinta):
    sql = "INSERT INTO hintaKaupassa (tuote_id, kauppa_id, hinta, paivays, kappalehinta) VALUES (%s,%s,%s,%s, %s)"
    db_command(sql, (tuote_id, kauppa_id, hinta, date, kappalehinta))


def select_kaupat(ketju):
    sql = "SELECT * FROM kauppa WHERE ketju = %s"
    return db_command(sql, [ketju])


def get_tuotteet():
    sql = "SELECT * FROM tuote"
    return novar_db_command(sql)


def get_historia(tuote):
    sql = "SELECT * from hintaHistoria where tuote_id = %s"
    return db_command(sql, [tuote])


def get_hinta(tuote_id, kauppa_id):
    sql = "SELECT * FROM hintaKaupassa WHERE tuote_id = %s AND kauppa_id = %s"
    return db_command(sql, (tuote_id, kauppa_id))


def update_hinta(tuote_id, kauppa_id, hinta, date, kappalehinta):
    sql = "UPDATE hintaKaupassa SET hinta = %s, paivays = %s, kappalehinta = %s WHERE tuote_id = %s AND kauppa_id = %s"
    return db_command(sql, (hinta, date, kappalehinta, tuote_id, kauppa_id))


def insert_historia(tuote_id, kauppa_id, hinta, date):
    sql = "INSERT INTO hintaHistoria (tuote_id, kauppa_id, hinta, alkupvm) VALUES (%s,%s,%s,%s)"
    return db_command(sql, (tuote_id, kauppa_id, hinta, date))


def hintavertailu(tuote_id, kauppa_id, hinta_nyt, kappalehinta):

    if len(get_hinta(tuote_id, kauppa_id)) == 0:
        hinta_tauluun(tuote_id, kauppa_id, hinta_nyt, date, kappalehinta)
    else:
        get = get_hinta(tuote_id, kauppa_id)[0]
        hist_hinta = get[3]
        hist_pvm = get[4]
        print(
            "Kantaan lähtee: TuoteID: "
            + str(tuote_id)
            + ", KauppaID: "
            + str(kauppa_id)
            + ", hinta: "
            + str(hinta_nyt)
            + "ja kappalehinta: "
            + str(kappalehinta),
        )
        insert_historia(tuote_id, kauppa_id, hist_hinta, hist_pvm)
        update_hinta(tuote_id, kauppa_id, hinta_nyt, date, kappalehinta)


def kloop(kauppa, kauppa_id, tuotteet):

    e = find_element(
        driver, "/html/body/div[1]/section/header/div[1]/nav/ul[1]/li[1]/a/span"
    )
    e.click()

    e = find_element(
        driver,
        "/html/body/div[1]/section/header/div[1]/nav/ul[2]/div/nav/div[2]/div/span/span",
    )
    e.click()
    e = find_element(driver, "/html/body/div[2]/div/div[2]/div[2]/form/div/div/input")
    e.send_keys(kauppa)
    sleep(3)
    e = find_element(
        driver, "/html/body/div[2]/div/div[2]/div[2]/div/div/a[1]/div[1]/div[2]"
    )
    e.click()
    khaku = driver.find_element_by_xpath(
        "/html/body/div[1]/section/section/div[2]/div[1]/div/div[2]/div/div[3]/input"
    )
    for t in tuotteet:

        khaku.clear()
        khaku.send_keys(t[3])
        sleep(2)

        try:
            e = ei_kkaupassa(
                driver,
                "/html/body/div[1]/section/section/div[2]/div[2]/div/div/div/div/div/div[1]/h1/span",
            )
            hintavertailu(t[0], kauppa_id, 99.99, 99.99)
        except ElementClickInterceptedException:
            print("Popupvittumitäpaskaa")
        except TimeoutException:
            for i in range(3):
                try:
                    e = find_element(
                        driver,
                        "/html/body/div[1]/section/section/div[2]/div[2]/div/div/div/div/div/ul/li[1]/div/a",
                    )
                    e.click()
                    e = find_element(
                        driver,
                        "/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/section[1]/div[1]/div/div[1]/span",
                    )
                    a = e.text.replace(",", ".")
                    e = find_element(
                        driver,
                        "/html/body/div[1]/section/section/div[2]/div[2]/section/section/div/div[1]/section/a",
                    )
                    e.click()
                    hintavertailu(t[0], kauppa_id, a, float(a) / int(t[2]))
                except ElementClickInterceptedException:
                    print("popupvittumitäpaskaa")
                    e = find_element(
                        driver, '//*[@id="giosg_live_chat_dialog"]/div[1]/div[1]/button'
                    )
                    e.click()
                    sleep(2)
                except NoSuchElementException:
                    pass
                    hintavertailu(t[0], kauppa_id, 99.99, 99.99)
                    break

                except TimeoutException:
                    pass
                    hintavertailu(t[0], kauppa_id, 99.99, 99.99)
                    break
                else:
                    break
            else:
                print("Miten vitussa??")


def sloop(kauppa, kauppa_id, tuotteet):

    e = find_element(
        d,
        "/html/body/div[5]/div[2]/header/div[3]/div/div[1]/div/nav/ul/li[4]/div/a/span",
    )
    e.click()
    sleep(10)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(kauppa)
    d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
    e = find_element(
        d,
        "/html/body/div[5]/div[2]/div[7]/div/div[3]/div[2]/div/ul/li[1]/div[1]/div[1]/a[2]",
    )
    e.click()
    e = find_element(d, "/html/body/div[5]/div[2]/header/div[2]/div/div/div/div/a")
    e.click()
    for t in tuotteet:
        d.find_element_by_xpath('//*[@id="multisearch-query"]').clear()
        d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(t[3])
        d.find_element_by_xpath('//*[@id="multisearch-query"]').send_keys(Keys.ENTER)
        sleep(10)

        try:
            e = ei_skaupassa(
                d, "/html/body/div[5]/div[2]/div[7]/div/div[2]/div[2]/div/div[2]/h2"
            )
            hintavertailu(t[0], kauppa_id, 99.99)
        except TimeoutException:
            try:
                e1 = find_element(
                    d,
                    "/html/body/div[5]/div[2]/div[7]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[1]",
                )
                e2 = find_element(
                    d,
                    "/html/body/div[5]/div[2]/div[7]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[1]/span[2]",
                )
                a = e1.text + "." + e2.text
                hintavertailu(t[0], kauppa_id, a, float(a) / int(t[2]))

            except NoSuchElementException:
                pass
                hintavertailu(t[0], kauppa_id, 99.99, 99.99)
                sleep(4)
            except TimeoutException:
                pass
                hintavertailu(t[0], kauppa_id, 99.99, 99.99)
                sleep(4)


date = datetime.datetime.now().strftime("%d.%m.%Y")
skaupat = select_kaupat("S-Ryhmä")
kkaupat = select_kaupat("Kesko")
tuotteet = get_tuotteet()

options = Options()
options.headless = True

driver = webdriver.Firefox(
    executable_path="/usr/local/bin/geckodriver", options=options
)
driver.get("https://www.k-ruoka.fi/")

for k in kkaupat:
    print("#" * 100)
    print(k[1])
    print(datetime.datetime.now().strftime("%H:%M:%S"))
    kloop(k[1], k[0], tuotteet)
driver.close()

d = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", options=options)
d.get("https://www.foodie.fi")
e = find_element(d, "/html/body/div[8]/div/div[2]/div/button[1]")
e.click()
sleep(2)

for s in skaupat:
    print("#" * 100)
    print(s[1])
    print(datetime.datetime.now().strftime("%H:%M:%S"))
    sloop(s[1], s[0], tuotteet)
d.close()

print(datetime.datetime.now().strftime("%H:%M:%S"))
