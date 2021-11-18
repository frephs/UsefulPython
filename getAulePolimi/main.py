'''
Made by Francesco Genovese
Edited by Paolo Ginefra

This program extrapolate a timetable of the free rooms in a given date at Polimi
'''

import requests
from bs4 import BeautifulSoup, builder
from datetime import date

from edifici import *

def getUrl(ed,gg, mm, yy):
    return "https://www7.ceda.polimi.it/spazi/spazi/controller/OccupazioniGiornoEsatto.do?csic="+str(ed)+"&categoria=tutte&tipologia=tutte&giorno_day="+str(gg)+"&giorno_month="+str(mm)+"&giorno_year="+str(yy)+"&jaf_giorno_date_format=dd%2FMM%2Fyyyy&evn_visualizza="

def getMatrixAule(ed, gg, mm, yy):
    # Returnig the data
    r = requests.get(getUrl(ed, gg, mm, yy))
    content = r.content

    # Let's get scraping
    soup = BeautifulSoup(content, 'html.parser')
    aule = soup.findAll('td', attrs = {'class':'data'})
    matrix = []
    for aula in aule:
        row = []
        #Appends the room's code
        row.append(aula.parent()[1].text.strip())
        ore = []
        for p in aula.parent():
            ## TODO: fix per le doppie righe negli orari
            if p.text != '':
                try:
                    #The number of time steps occupied by lecture
                    quarters = int(p.attrs['colspan'])
                    ore += [1] * quarters
                except:
                    pass
            else:
                ore += [0]

        row.append(ore) #One hot encoded time table (1 - occupied, 0 - free)
        matrix.append(row)
    return matrix

def getAdvice(ed,gg, mm, yy, threshold):

    #Checks whether a room is free for at least "threshold" hours
    def check(hStart, hFin, threshold, advice):
        if hFin-hStart >= threshold:
                    advice.append([str(int(hStart))+':'+str(int(hStart*60%60)), str(int(hFin))+':'+f"{int(hFin*60%60):02}", hFin-hStart])

    #Let's get counting
    matrix = getMatrixAule(ed,gg, mm, yy)
    advices = []
    for aula in matrix:
        advice = [aula[0]]
        hStart = 8
        hFin = hStart
        for busy in aula[1]:
            if not busy :
                hFin += 0.25
            else:
                check(hStart, hFin, threshold, advice)
                hStart = hFin + 0.25
                hFin = hStart
        check(hStart, hFin, threshold, advice)

        #Adding a room only if it has free hours
        if len(advice) > 1:
            advices.append(advice)

        # Sorting by number of hours
        def returnHours(elem):
            return elem[1][2]

        advices.sort(key=returnHours, reverse=True)

    return advices

def printAdvice(advices):
    for advice in advices:
        print(advice)

def main():
    t = date.today()
    building = "MIA"
    print("=======================================")
    print("Free rooms in " + building + " - " + edifici[building])
    print("=======================================")
    print("--------")
    print("TODAY")
    print("---------")
    printAdvice(getAdvice(building, t.day, t.month, t.year, 3))
    print("--------")
    print("TOMORROW")
    print("---------")
    printAdvice(getAdvice(building, t.day+1, t.month, t.year, 3))

if __name__ == "__main__":
    main()
