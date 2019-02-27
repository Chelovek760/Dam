import matplotlib.pyplot as plt
import Grafiki_Ischod
import random
import datetime
import math


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

    def compare(self, current_Level, prit):
        # if current_Level<self.NPU*1.05 and current_Level>self.NPU*0.95:
        #   return 1
        if current_Level < self.NPU * 1.00001 and current_Level > self.NPU * 0.9999999:
            return prit / V_to_H(self.MAX_SBROS, self.S_ZERKALA)
        else:
            if self.NPU > current_Level:
                # print(current_Level-self.UMO,'1')
                if (current_Level - self.UMO) > 0:
                    return math.log(((current_Level - self.UMO)) / (self.NPU - self.UMO))
                else:
                    return 0
            else:
                # print(self.FPU-current_Level,'2')
                if (self.FPU - current_Level) > 0:
                    return -(math.log(1 - (self.FPU - current_Level) / (self.FPU - self.NPU)))
                else:
                    return 1

    def quality(self):
        pass

    def delay(self, proctreb, procnow, TIME_FOR_FULL_OPEN):
        proc_v_sec=100 / TIME_FOR_FULL_OPEN
        if abs(proctreb-procnow)>proc_v_sec:
            if proctreb > procnow:
                procnow = procnow + proc_v_sec
            if proctreb < procnow:
                procnow = procnow - proc_v_sec
            if proctreb == procnow:
                procnow = proctreb
            return procnow
        else:
            return proctreb

    def proc_otkr_zaslonki(self, pritok):
        proc = H_to_V(pritok, self.S_ZERKALA) / self.MAX_SBROS
        if proc > 1:
            proc = 1
        # print('Peregruz')
        # print(proc,'pritok',pritok,'Max',self.MAX_SBROS)
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
    file_name = 'D:\Ботать\Проганье\Плотины\GES_DATA.json'
    DATA = Grafiki_Ischod.get_struct(file_name)
    period = 5
    deltatime = datetime.timedelta(period)
    dateStart = datetime.datetime(2018, 6, 1)
    datenow = dateStart
    time = 24 * 60 * 60
    levels = []
    name = 'rybinsk'
    pritoki = []
    raschodi = []
    procs_open = []
    proc_treb = []
    levels_vchod = []
    datenow_str = str(datenow)
    ges1 = GES(DATA[name][datenow_str], 4550 * 1000 * 1000,
               1000)
    current_level = ges1.Level
    times = [i for i in range(1, time)]
    proc_now = 0
    proc_treb=[]
    while datenow - dateStart < deltatime:
        datenow_str = str(datenow)
        print('Date\n', datenow, '\n')
        ges1 = GES(DATA[name][datenow_str], 4550 * 1000 * 1000,
                   1000)
        # current_level = raspred_na_den_with_noise(current_level)
        print('NPU', ges1.NPU)
        for _ in times:
            prit = V_to_H(raspred_na_den_with_noise(ges1.PRITOK), ges1.S_ZERKALA, )
            # print("prit")
            # raschod = V_to_H(raspred_na_den_with_noise(ges1.FULL_RASHOD),ges1.S_ZERKALA,)
            # print('raschod')
            current_level = prit + current_level
            proc_treb.append(abs(ges1.compare(current_level,prit)))
            proc_now = ges1.delay(abs(ges1.compare(current_level, prit)), proc_now, 600000)
            raschod = V_to_H(ges1.MAX_SBROS, ges1.S_ZERKALA) *proc_now
            # current_level = current_level - V_to_H(ges1.MAX_SBROS,ges1.S_ZERKALA) * ges1.proc_otkr_zaslonki(prit)
            current_level = current_level - raschod
            # print(current_level)
            levels.append(current_level)
            pritoki.append(prit)
            raschodi.append(raschod)
            procs_open.append(proc_now)
        datenow = datenow + datetime.timedelta(1)
    #print(procs_open)
    #print(proc_treb)
    #print(raschodi)
    plt.plot([i for i in range(len(levels))], levels, label='Level Now')
    plt.plot([i for i in range(len(levels))], [ges1.NPU for _ in range(len(levels))], label='Opt')
    plt.legend()
    plt.grid()
    fig = plt.figure()
    plt.plot([i for i in range(len(levels))], pritoki, label='pritok')
    plt.plot([i for i in range(len(levels))], raschodi, label='rashod')
    plt.legend()
    fig = plt.figure()
    plt.plot([i for i in range(len(levels))], procs_open, label='proc_now')
    plt.plot([i for i in range(len(levels))], proc_treb, label='proc_rteb')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
