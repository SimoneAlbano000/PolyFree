"""
Free rooms in Polito
"""
import re
import requests
import base64
from bs4 import BeautifulSoup

import toga
from toga.style import Pack
from toga.constants import RED, GREY
from toga.style.pack import COLUMN, ROW, BOTTOM

def getRooms():
    # Get times and rooms number from swasPolito
    while(1):
        try:
            page = requests.get('https://www.swas.polito.it/dotnet/orari_lezione_pub/RicercaAuleLiberePerFasceOrarie.aspx')
            break
        except:
          pass
    ## ---------------------------------------------------------------------------
    soup = BeautifulSoup(page.text, 'html.parser')
    roomsTable = soup.find(class_='ListElement')
    roomsTime = roomsTable.find_all('span', id=re.compile("Pagina_gv_AuleLibere_lbl_FasciaOraria_"))
    roomsFree = roomsTable.find_all('span', id=re.compile("Pagina_gv_AuleLibere_lbl_AuleLibere_"))
    # Extract only the required data
    timesList = []
    for time in roomsTime:
        timesList.append(str(time.contents).lstrip("['").rstrip("']").split(','))
    # ---------------------------------------------------------------------------
    roomsList = []
    for room in roomsFree:
        # Check for empty spans
        if(len(room.contents)==0):
            room.contents = ["Empty"]
        roomsList.append(str(room.contents).lstrip("['").rstrip("']").split(','))
    # ---------------------------------------------------------------------------
    return (timesList, roomsList)

def SubtractRooms(dataSet: tuple):
    resRoomList = []
    resRoomList.append(["Empty"])
    for element in range(0, len(dataSet)-1, 1):
        # Check for "Empty" lists
        # -------------------------------
        if(dataSet[element][0]=="Empty"):
            set1 = set()
        else:
            set1 = set(dataSet[element])
        # -------------------------------
        if(dataSet[element+1][0]=="Empty"):
            set2 = set()
        else:
            set2 = set(dataSet[element+1])
        # -------------------------------
        # Subtract the sets
        for room in set1:
            set2.discard(room)
        # Check again for "Empty" sets
        if(len(set2)==0):
            set2.add("Empty")
        resRoomList.append(list(set2))
    return resRoomList

def getRev():
    rev_url = 'https://api.github.com/repos/SimoneAlbano000/PolyFree/contents/app.rev'
    req = requests.get(rev_url)
    if(req.status_code == requests.codes.ok):
        req = req.json()
        app_rev = str((base64.b64decode(req['content']))).lstrip("b'").rstrip("'")
    else:
        app_rev = "Not Found"
    return str(app_rev)

class PolyFree(toga.App):
    def startup(self):
        # Checking revision ----------------------------------------------------
        git_rev = getRev()
        this_rev = '1.0.9'
        if(git_rev != this_rev):
            rev = 'New version available! ('+ git_rev + ')'
            rev_lable_color = RED
        else:
            rev = this_rev
            rev_lable_color = GREY
        # ----------------------------------------------------------------------
        # UI variables
        text_size = 18

        # Create the main container for all the pages
        main_box = toga.Box(style=Pack(direction=COLUMN))
        data_box = toga.Box(style=Pack(direction=COLUMN))
        dev_box = toga.Box(style=Pack(direction=COLUMN))

        headings = ['Times:', 'Rooms:']
        data = []
        # Add our data(Free now) to a Table, ready to be returned
        rooms_table_free_now = toga.Table(headings, data=data, missing_value='Data unavailable', style=Pack(font_size=text_size))
        # Add our data(Available from now) to a Table, ready to be returned
        rooms_table_lecture_ended_now = toga.Table(headings, data=data, missing_value='Data unavailable', style=Pack(font_size=text_size))

        # Obtain the rooms data
        tupleOfData = getRooms()
        roomsAvailableNow = tupleOfData[1]
        roomsLectureEndedNow = SubtractRooms(tupleOfData[1])

        for i in range(0, len(tupleOfData[0]), 1):
            # Compose all the data into the tables
            rooms_table_free_now.data.append(''.join(tupleOfData[0][i]), ', '.join(roomsAvailableNow[i]))
            rooms_table_lecture_ended_now.data.append(''.join(tupleOfData[0][i]), ', '.join(roomsLectureEndedNow[i]))
            pass

        # Add the tables to the main container, and dev info
        dev_label = toga.Label('dev: Starlightlicious', style=Pack(font_size=text_size))
        rev_label = toga.Label('rev: ' + rev, style=Pack(font_size=text_size, color=rev_lable_color))
        dev_box.add(dev_label) 
        dev_box.add(rev_label)
        topLable = toga.Label('Rooms available at the moment:', style=Pack(font_size=text_size))
        data_box.add(topLable)
        data_box.add(rooms_table_free_now)
        middleLable = toga.Label('Rooms in which lesson ends now:', style=Pack(font_size=text_size))
        data_box.add(middleLable)
        data_box.add(rooms_table_lecture_ended_now)

        main_box.add(data_box)
        main_box.add(dev_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return PolyFree(
        formal_name='PolyFree',
        app_name='PolyFree',
    )
