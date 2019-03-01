import json
import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import dates


def get_struct(file_name):
    with open(file_name,'r') as f:
        DATA_FULL=json.load(f)
    return DATA_FULL


def main():
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Calibri'
    sis = sys.platform
    if sis == 'win32':
        file_name = os.getcwd() + '\\GES_DATA.json'
    else:
        file_name = os.getcwd() + '/GES_DATA.json'
    DATA=get_struct(file_name)
    WHAT_GRAF="Level"
    #for name in DATA:
    for name in DATA:
        date=[]
        levels=[]
        for datem in DATA[name]:
            date.append(dates.date2num(datetime.strptime(datem[:-9],'%Y-%m-%d')))
            levels.append(DATA[name][datem][WHAT_GRAF])
        plt.figure()
        axes = plt.subplot(1, 1, 1)
        axes.xaxis.set_major_formatter (dates.DateFormatter("%d.%m.%y"))
        plt.plot(date,levels)
        plt.grid()
        figname=name+"_"+WHAT_GRAF+".png"
        plt.savefig(figname, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()
