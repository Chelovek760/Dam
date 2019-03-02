import datetime
import os
import random
import sys

import math
import matplotlib.pyplot as plt

import Grafiki_Ischod


class GES():
    def __init__(self, DATA, S_ZERKALA, MAX_SBROS):
        self.FPU = DATA['FPU']
        self.NPU = DATA['NPU']
        self.UMO = DATA['UMO']
        self.Level = DATA['Level']
        self.FREE_V = DATA['FREE_V']
        self.PRITOK = DATA['PRITOK']
        self.FULL_RASHOD = DATA['FULL_RASHOD']
        self.S_ZERKALA = S_ZERKALA
        self.MAX_SBROS = MAX_SBROS

    def compare(self, current_Level, prit, rashod, proc_now, TIME_FOR_FULL_OPEN):
        MIN_RASHOD = 1 * 10 ** (-7)
        if current_Level < self.NPU * 1.01 and current_Level > self.NPU * 0.99:
            treb_proc = prit / V_to_H(self.MAX_SBROS, self.S_ZERKALA)
            if treb_proc * V_to_H(self.MAX_SBROS, self.S_ZERKALA) < MIN_RASHOD:
                treb_proc = MIN_RASHOD / V_to_H(self.MAX_SBROS, self.S_ZERKALA)
            if treb_proc > 1:
                treb_proc = 1
            return treb_proc
        else:
            if self.NPU > current_Level:
                if (current_Level - self.UMO) > 0:

                    treb_proc = math.sqrt((-(math.log10((current_Level - self.UMO) / (self.NPU - self.UMO)))) ** 2 + (
                                prit / V_to_H(self.MAX_SBROS, self.S_ZERKALA)) ** 2)
                    # print(treb_proc, 'menishe')
                    # print(prit,rashod)
                    # if prit * self.delay(treb_proc, proc_now, TIME_FOR_FULL_OPEN) * self.MAX_SBROS > rashod:
                    #  treb_proc = prit / V_to_H(self.MAX_SBROS, self.S_ZERKALA)*abs(rashod-prit)
                    if treb_proc * V_to_H(self.MAX_SBROS, self.S_ZERKALA) < MIN_RASHOD:
                        treb_proc = MIN_RASHOD / V_to_H(self.MAX_SBROS, self.S_ZERKALA)
                    if treb_proc <= 0:
                        treb_proc = 0
                    if treb_proc > 1:
                        treb_proc = 1

                    return treb_proc

                else:
                    return 0
            else:
                if (self.FPU - current_Level) > 0:
                    treb_proc = math.sqrt((-(math.log10((current_Level - self.UMO) / (self.NPU - self.UMO)))) ** 2 + (
                                prit / V_to_H(self.MAX_SBROS, self.S_ZERKALA)) ** 2)
                    # print(treb_proc, 'Bol')
                    # if prit * self.delay(treb_proc, proc_now, TIME_FOR_FULL_OPEN) * self.MAX_SBROS > rashod:
                    #   treb_proc = prit / V_to_H(self.MAX_SBROS, self.S_ZERKALA) * abs(rashod - prit)
                    if self.delay(treb_proc, proc_now, TIME_FOR_FULL_OPEN) * V_to_H(self.MAX_SBROS,
                                                                                    self.S_ZERKALA) < MIN_RASHOD:
                        treb_proc = MIN_RASHOD / V_to_H(self.MAX_SBROS, self.S_ZERKALA)

                    if treb_proc <= 0:
                        treb_proc = 0
                    if treb_proc > 1:
                        treb_proc = 1

                    return treb_proc
                else:
                    return 1

    def quality(self):
        pass

    def delay(self, proctreb, procnow, TIME_FOR_FULL_OPEN):
        proc_v_sec = 1 / TIME_FOR_FULL_OPEN
        if proctreb < 0:
            return 0

        if abs((proctreb - procnow)) > proc_v_sec:
            if proctreb > procnow:
                procnow = procnow + proc_v_sec
            if proctreb < procnow:
                procnow = procnow - proc_v_sec
            return procnow
        else:
            return proctreb

    def proc_otkr_zaslonki(self, pritok):
        proc = H_to_V(pritok, self.S_ZERKALA) / self.MAX_SBROS
        if proc > 1:
            proc = 1
        return proc


def raspred_na_den_with_noise(voda_v_sec):
    # print('Shum',random.gauss(0, 1) * 0.05 * voda_v_sec,'Voda',voda_v_sec )
    return random.gauss(0, 1) * 0.05 * voda_v_sec + voda_v_sec


def V_to_H(V, S):
    return V / S


def H_to_V(H, S):
    return H * S


def momental_rash_prolong_na_den(voda_v_sec):
    return voda_v_sec * 24 * 60 * 60


def main():
    sis = sys.platform
    if sis == 'win32':
        file_name = os.getcwd() + '\\GES_DATA.json'
    else:
        file_name = os.getcwd() + '/GES_DATA.json'
    DATA = Grafiki_Ischod.get_struct(file_name)
    period = 10
    S_ZERKALA_1 = 4550 * 1000 * 1000
    MAX_RASHOD_1 = 1000
    VREMYA_POLNOGO_OTKR_1 = 100
    S_ZERKALA_2 = 1591 * 1000 * 1000
    MAX_RASHOD_2 = 1000
    VREMYA_POLNOGO_OTKR_2 = 60
    S_ZERKALA_3 = 1508 * 1000 * 1000
    MAX_RASHOD_3 = 1000
    VREMYA_POLNOGO_OTKR_3 = 60
    deltatime = datetime.timedelta(period)
    dateStart = datetime.datetime(2017, 9, 1)
    datenow = dateStart
    time = 24*60*60
    levels = []
    name = 'rybinsk'
    name1 = 'nijegorod'
    name2 = 'cheboksar'
    levels1 = []
    levels2 = []
    levels3 = []
    pritok1 = []
    pritok2 = []
    pritok3 = []
    raschod1mas = []
    raschod2mas = []
    raschod3mas = []
    datenow_str = str(datenow)
    ges1 = GES(DATA[name][datenow_str], S_ZERKALA_1, MAX_RASHOD_1)
    ges2 = GES(DATA[name1][datenow_str], S_ZERKALA_2, MAX_RASHOD_2)
    ges3 = GES(DATA[name2][datenow_str], S_ZERKALA_3, MAX_RASHOD_3)
    current_levels = [ges1.Level, ges2.Level, ges3.Level]
    times = [i for i in range(1, time)]
    proc_now1 = 0
    proc_now2 = 0
    proc_now3 = 0
    raschod1 = 0
    raschod2 = 0
    raschod3 = 0
    while datenow - dateStart < deltatime:
        datenow_str = str(datenow)
        print('Date\n', datenow, '\n')
        ges1 = GES(DATA[name][datenow_str], S_ZERKALA_1, MAX_RASHOD_1)
        ges2 = GES(DATA[name1][datenow_str], S_ZERKALA_2, MAX_RASHOD_2)
        ges3 = GES(DATA[name2][datenow_str], S_ZERKALA_3, MAX_RASHOD_3)
        # current_level = raspred_na_den_with_noise(current_level)
        # print('NPU', ges1.NPU, ges2.NPU, ges3.NPU)
        for _ in times:
            prit = V_to_H(raspred_na_den_with_noise(ges1.PRITOK), ges1.S_ZERKALA, )
            pritok1.append(prit)
            current_level = prit + current_levels[0]
            # proc_treb.append((ges1.compare(current_level, prit, raschod1, proc_now, VREMYA_POLNOGO_OTKR_1)))
            proc_now1 = ges1.delay((ges1.compare(current_level, prit, raschod1, proc_now1, VREMYA_POLNOGO_OTKR_1)),
                                   proc_now1, VREMYA_POLNOGO_OTKR_1)
            # print(proc_now)
            raschod1 = V_to_H(ges1.MAX_SBROS, ges1.S_ZERKALA) * proc_now1
            raschod1mas.append(raschod1)
            current_levels[0] = current_level - raschod1
            prit = V_to_H(H_to_V(raspred_na_den_with_noise(raschod1), ges1.S_ZERKALA, ),
                          ges2.S_ZERKALA)
            # print(raschod,prit)
            pritok2.append(prit)
            current_level = prit + current_levels[1]
            # proc_treb.append((ges2.compare(current_level, prit, raschod2, proc_now2, VREMYA_POLNOGO_OTKR_2)))
            proc_now2 = ges2.delay((ges2.compare(current_level, prit, raschod2, proc_now2, VREMYA_POLNOGO_OTKR_2)),
                                   proc_now2, VREMYA_POLNOGO_OTKR_2)
            raschod2 = V_to_H(ges2.MAX_SBROS, ges2.S_ZERKALA) * proc_now2
            raschod2mas.append(raschod2)
            current_levels[1] = current_level - raschod2
            prit = V_to_H(H_to_V(raspred_na_den_with_noise(raschod2), ges2.S_ZERKALA, ),
                          ges3.S_ZERKALA)
            pritok3.append(prit)
            current_level = prit + current_levels[2]
            # proc_treb.append((ges3.compare(current_level, prit, raschod3, proc_now3, VREMYA_POLNOGO_OTKR_3)))
            proc_now3 = ges3.delay((ges3.compare(current_level, prit, raschod3, proc_now3, VREMYA_POLNOGO_OTKR_3)),
                                   proc_now3, VREMYA_POLNOGO_OTKR_3)
            raschod3 = V_to_H(ges3.MAX_SBROS, ges3.S_ZERKALA) * proc_now3
            raschod3mas.append(raschod3)
            current_levels[2] = current_level - raschod3
            levels1.append(current_levels[0])
            levels2.append(current_levels[1])
            levels3.append(current_levels[2])
            # procs_open.append(proc_now)
            # print(proc_now,proc_now2,proc_now3)
        datenow = datenow + datetime.timedelta(1)
        # print(raschod1,raschod3)
    # print(procs_open)
    # print(proc_treb)
    # print(raschodi)
    # levels = [levels1, levels2, levels3]
    # print(levels2)
    fig = plt.figure()
    plt.plot([i for i in range(len(levels1))], levels1, label='Level Now')
    plt.plot([i for i in range(len(levels1))], [ges1.NPU for _ in range(len(levels1))], label='Opt')
    plt.legend()
    plt.grid()
    plt.savefig('1.png')
    fig = plt.figure()
    plt.plot([i for i in range(len(levels2))], levels2, label='Level Now')
    plt.plot([i for i in range(len(levels2))], [ges2.NPU for _ in range(len(levels2))], label='Opt')
    plt.legend()
    plt.grid()
    plt.savefig('2.png')
    fig = plt.figure()
    plt.plot([i for i in range(len(levels3))], levels3, label='Level Now')
    plt.plot([i for i in range(len(levels3))], [ges3.NPU for _ in range(len(levels3))], label='Opt')
    plt.legend()
    plt.grid()
    plt.savefig('3.png')
    fig = plt.figure()
    plt.plot([i for i in range(len(levels1))], pritok1, label='prit')
    plt.plot([i for i in range(len(levels1))], raschod1mas, label='raschd')
    plt.legend()
    plt.grid()
    plt.savefig('4.png')
    fig = plt.figure()
    plt.plot([i for i in range(len(levels2))], pritok2, label='prit')
    plt.plot([i for i in range(len(levels2))], raschod2mas, label='raschd')
    plt.legend()
    plt.grid()
    plt.savefig('5.png')
    fig = plt.figure()
    plt.plot([i for i in range(len(levels3))], pritok3, label='prit')
    plt.plot([i for i in range(len(levels3))], raschod3mas, label='rashod')
    plt.legend()
    plt.grid()
    plt.savefig('6.png')
    '''for level in levels:
        fig = plt.figure()
        plt.plot([i for i in range(len(level))], level, label='Level Now')
        plt.plot([i for i in range(len(level))], [ges1.NPU for _ in range(len(level))], label='Opt')
    fig = plt.figure()
    plt.plot([i for i in range(len(levels))], pritoki, label='pritok')
    plt.plot([i for i in range(len(levels))], raschodi, label='rashod')
    plt.legend()
    fig = plt.figure()
    plt.plot([i for i in range(len(levels))], procs_open, label='proc_now')
    plt.plot([i for i in range(len(levels))], proc_treb, label='proc_rteb')
    plt.legend()'''
    plt.show()


if __name__ == '__main__':
    main()
