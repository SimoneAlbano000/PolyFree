"""
Free rooms in Polito
"""
import re
import requests
from bs4 import BeautifulSoup

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, BOTTOM

def getRooms():
    # Get times and rooms number from swasPolito
    while(1):
        try:
            page = requests.get('https://www.swas.polito.it/dotnet/orari_lezione_pub/RicercaAuleLiberePerFasceOrarie.aspx')
            break
        except:
          pass  
    soup = BeautifulSoup(page.text, 'html.parser')
    roomsTable = soup.find(class_='ListElement')
    roomsTime = roomsTable.find_all('span', id=re.compile("Pagina_gv_AuleLibere_lbl_FasciaOraria_"))
    roomsFree = roomsTable.find_all('span', id=re.compile("Pagina_gv_AuleLibere_lbl_AuleLibere_"))
    # Extract only the required data
    timesList = []
    for time in roomsTime:
        timesList.append(time.contents[0])
    roomsList = []
    for room in roomsFree:
        roomsList.append(room.contents[0])
    # Return a tuple
    return (timesList, roomsList, len(timesList))

def getRoomsNextAvailable(data):
    # Subtract the 'i' free rooms from the 'i+1' rooms list
    # Trasform list into vector of rooms
    str2list = []
    list2str = []
    list2str.append('Empty')
    # Convert string to list
    for rooms in data[1]:
        str2list.append(rooms.split(','))
    # Make subtration
    for i in range(0, data[2]-1, 1):
        set1 = set(str2list[i])
        set2 = set(str2list[i+1])
        for j in set1:
            set2.discard(j)
        # Check for empty sets
        if(len(set2)==0):
            set2.add('Empty')
        list2str.append(','.join(list(set2)))
    return list2str

class PolyFree(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        data_box = toga.Box(style=Pack(direction=COLUMN))
        dev_box = toga.Box(style=Pack(direction=COLUMN))
        text_size = 18
        rev = '1.0.7'
        # Create the main container for all the pages
        # __removed__ container = toga.OptionContainer()
        
        headings = ['Times:', 'Rooms:']
        data = []
        # Add our data(Free now) to a Table, ready to be returned
        rooms_table_free_now = toga.Table(headings, data=data, missing_value='Data unavailable', style=Pack(font_size=text_size))
        # Add our data(Available from now) to a Table, ready to be returned
        rooms_available_from_now = toga.Table(headings, data=data, missing_value='Data unavailable', style=Pack(font_size=text_size))

        # Obtain the rooms data
        roomsData_freeNow = getRooms()
        roomsData_available_from_now = getRoomsNextAvailable(roomsData_freeNow)

        for i in range(0, roomsData_freeNow[2], 1):
            # Compose all the data into the tables
            rooms_table_free_now.data.append(str(roomsData_freeNow[0][i]), str(roomsData_freeNow[1][i]))
            rooms_available_from_now.data.append(str(roomsData_freeNow[0][i]), str(roomsData_available_from_now[i]))
        # Add the tables to the main container
        # __removed__ container.add('Free now', rooms_table_free_now)
        # __removed__ container.add('Available from now', rooms_available_from_now)   
        
        #add dev info
        dev_label = toga.Label('dev: Starlightlicious, rev: '+rev, style=Pack(font_size=text_size))
        dev_box.add(dev_label) 
        topLable = toga.Label('Rooms available at the moment:', style=Pack(font_size=text_size))
        data_box.add(topLable)
        data_box.add(rooms_table_free_now)
        middleLable = toga.Label('Rooms available from now on:', style=Pack(font_size=text_size))
        data_box.add(middleLable)
        data_box.add(rooms_available_from_now)

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
