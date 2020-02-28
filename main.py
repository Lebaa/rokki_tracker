from selenium import webdriver
from time import sleep
import datetime

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
    time = str(datetime.datetime.now().time()).split(".")[0]
    e = Entry(artist,song,time)
    return e


driver = webdriver.Firefox()
driver.get("https://www.supla.fi/radiorock")
driver.find_element_by_xpath('//*[@id="sccm-opt-out-c1"]').click()

while datetime.datetime.now().hour > 5 and datetime.datetime.now().hour < 18:

    nowPlaying = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/section[1]/div/div[2]/div[2]/div').text
    s = (Parser(nowPlaying).artist + "\n"+ Parser(nowPlaying).song +"\n"+ Parser(nowPlaying).timestamp)

    biisi = Parser(nowPlaying).song
    if biisi not in played:
        if len(played) < 15:
            played.append(Parser(nowPlaying).song)
            print(played)
            sleep(120)
        else:
            print("Vitusti kamaa listalla, tyhjennetään")
            played.clear()
            played.append(Parser(nowPlaying).song)
            print(played)

    else:
        sleep(120)

print("Aika täynnä")









