from selenium import webdriver
import time
from time import sleep
import datetime
import MySQLdb as mysql
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


played = []

class Entry():
    def __init__(self,artist,song,timestamp):
        self.artist = artist
        self.song = song
        self.timestamp = timestamp

def Parser(nowPlaying):
    s = nowPlaying.split("music_note")
    d = s[1].split("-",1)
    artist = d[0]
    song = d[1].lstrip()
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    e = Entry(artist,song,timestamp)
    return e

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
            database="Leba$rokki",
        )

        cur = connection.cursor()
        cur.execute(command, variables)
        result = cur.fetchall()
        connection.commit()
        connection.close()
        return result

def insert_biisi(artisti, kappale, timestamp):
    sql = "INSERT INTO biisi (artisti, kappale, timestamp) VALUES (%s,%s,%s)"
    db_command(sql, (artisti, kappale, timestamp))


driver = webdriver.Firefox()
driver.get("https://www.supla.fi/radiorock")
driver.find_element_by_xpath('//*[@id="sccm-opt-out-c1"]').click()

while datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 18:

    nowPlaying = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/section[1]/div/div[2]/div[2]/div').text
    s = (Parser(nowPlaying).artist + "\n"+ Parser(nowPlaying).song +"\n"+ Parser(nowPlaying).timestamp)

    biisi = Parser(nowPlaying).song
    if biisi not in played:
        if len(played) < 5:
            obj = Parser(nowPlaying)
            insert_biisi(obj.artist, obj.song, obj.timestamp)
            played.append(obj.song)
            print(played)
            sleep(120)
        else:
            print("Vitusti kamaa listalla, tyhjennetään")
            obj = Parser(nowPlaying)
            insert_biisi(obj.artist, obj.song, obj.timestamp)
            played.append(obj.song)
            print(played)

    else:
        sleep(120)

print("Aika täynnä")









