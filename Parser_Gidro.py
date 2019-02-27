from datetime import datetime,timedelta
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas

def get_html(url):
    response = requests.get(url)
    return response.text


def text_before_word(text, word):
    line = text.split(word)[0].strip()
    return line


def get_page_data(html,Data_Full,date):
    soup = BeautifulSoup(html, 'lxml')
    name=soup.find_all('div',class_=re.compile('informer-block \w*'))
    for mas in name:
        NAME=mas.get('class')[1]
        if NAME not in Data_Full:
            Data_Full[NAME]=dict()

        FPU = mas.find('p').next_element.next_element.next_element.text[:-2].replace(',', '.')
        FPU = FPU.strip()
        try:
            FPU = float(FPU)
        except BaseException:
            FPU=0

        NPU = mas.find('p').findNext('p').next_element.next_element.next_element.text[:-2].replace(',', '.')
        NPU = NPU.strip()
        try:
            NPU = float(NPU)
        except BaseException:
            NPU=0

        UMO = mas.find('p').findNext('p').findNext('p').next_element.next_element.next_element.text[:-2].replace(
            ',', '.')
        UMO = UMO.strip()
        try:
            UMO = float(UMO)
        except BaseException:
            UMO=0

        Level = mas.find('p').findNext('p').findNext('p').findNext('p').next_element.next_element.text[:-2].replace(
            ',', '.')
        Level = Level.strip()
        try:
            Level = float(Level)
        except BaseException:
            Level=0

        FREE_V = mas.find('p').findNext('p').findNext('p').findNext('p').findNext(
            'p').next_element.next_element.text[:-7].replace(',', '.') + '000000'
        FREE_V = FREE_V.strip()
        try:
            FREE_V = float(FREE_V)
        except BaseException:
            FREE_V=0

        PRITOK = mas.find('p').findNext('p').findNext('p').findNext('p').findNext('p').findNext(
            'p').next_element.next_element.text[:-4].replace(',', '.')
        PRITOK = PRITOK.strip()
        try:
            PRITOK = float(PRITOK)
        except BaseException:
            PRITOK=0

        FULL_RASHOD = mas.find('p').findNext('p').findNext('p').findNext('p').findNext('p').findNext('p').findNext(
            'p').next_element.next_element.text[:-4].replace(',', '.')
        FULL_RASHOD = FULL_RASHOD.strip()
        try:
            FULL_RASHOD = float(FULL_RASHOD)
        except BaseException:
            FULL_RASHOD=0

        RASHOD_VODOZBROS = mas.find('p').findNext('p').findNext('p').findNext('p').findNext('p').findNext(
            'p').findNext('p').findNext('p').next_element.next_element.text[:-4].replace(',', '.')
        RASHOD_VODOZBROS = RASHOD_VODOZBROS.strip()
        try:
            RASHOD_VODOZBROS = float(RASHOD_VODOZBROS)
        except BaseException:
            RASHOD_VODOZBROS=0
        Data_Full[NAME][date]=[]
        Data_Full[NAME][date]= {'FPU': FPU, 'NPU': NPU,'UMO':UMO, 'Level': Level, 'FREE_V': FREE_V, 'PRITOK': PRITOK, 'FULL_RASHOD': FULL_RASHOD,
             'RASHOD_VODOZBROS': RASHOD_VODOZBROS}

    #for i in Data_Full:
        #print(Data_Full[i],'\n')
    return Data_Full


def write_to_file(data):
    with open('GES_DATA.json', 'w') as f:
        json.dump(data,f)
    with pandas.ExcelWriter('GES_DATAv2.xlsx') as writer:
        for name in data:
            pandas.DataFrame(data[name]).to_excel(writer,sheet_name=name)


def main():
    Full_Date=dict()
    dateStart=datetime(2013,4,13)
    while dateStart< datetime.now()-timedelta(1):
        print(dateStart.strftime("%Y-%m-%d"))
        link='http://www.rushydro.ru/hydrology/informer/?date='+str(dateStart.strftime("%Y-%m-%d"))
        html=get_html(link)
        #with open(str(dateStart.strftime("%Y-%m-%d"))+'.html','w',encoding='utf-8') as f:
            #f.write(html)
        Full_Date=get_page_data(html,Full_Date,str(dateStart))
        dateStart=dateStart+timedelta(1)
    write_to_file(Full_Date)
    '''for i in Full_Date:
        for date in Full_Date[i]:
            print(Full_Date[i][date]['Level'])
        print(i,'\n')'''
if __name__ == '__main__':
    main()
