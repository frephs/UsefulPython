import requests
from bs4 import BeautifulSoup

def getUrl(ed,gg, mm, yy):
    print("https://www7.ceda.polimi.it/spazi/spazi/controller/OccupazioniGiornoEsatto.do?csic="+str(ed)+"&categoria=tutte&tipologia=tutte&giorno_day="+str(gg)+"&giorno_month="+str(mm)+"&giorno_year="+str(yy)+"&jaf_giorno_date_format=dd%2FMM%2Fyyyy&evn_visualizza=")
    return "https://www7.ceda.polimi.it/spazi/spazi/controller/OccupazioniGiornoEsatto.do?csic=MIA&categoria=tutte&tipologia=tutte&giorno_day="+str(gg)+"&giorno_month="+str(mm)+"&giorno_year="+str(yy)+"&jaf_giorno_date_format=dd%2FMM%2Fyyyy&evn_visualizza="

def getMatrixAule(ed,gg, mm, yy):
    r = requests.get(getUrl(ed, gg, mm, yy))
    content = r.content
    soup = BeautifulSoup(content, 'html5lib')
    aule = soup.findAll('td', attrs = {'class':'data'})
    matrix = [];
    for aula in aule:
        row = []
        row.append(aula.parent()[1].text.strip())
        ore = [];
        n = len(aula.parent())
        i=2; h=8; d=0; m=0;
        while i<n:
            ## TODO:FIX PER LE DOPPIE RIGHE NEGLI ORARI
            if aula.parent()[i].text != '':
                try:
                    quarters = int(aula.parent()[i].attrs['colspan']);
                    for t in range(quarters):
                        ore.append(1)
                except:
                    pass
            else:
                ore.append(0);
            i +=1;
        row.append(ore)
        matrix.append(row)
        # for rows in matrix:
        #     for col in rows:
        #         print(col)
        # print(len(matrix))
    return matrix;

def getAdvice(ed,gg, mm, yy, threshold):
    matrix = getMatrixAule(ed,gg, mm, yy)
    advices = [];
    for aula in matrix:
        advice = []
        hStart = 8;
        hFin = hStart;
        wasFree = 1;
        i=0;
        for busy in aula[1]:
            if not busy :
                hFin += 0.25;
                wasFree=1
            else:
                if wasFree and hFin-hStart >= threshold: #seleziono le aule libere per più di un'ora e mezza
                    if len(advice) ==0:
                        advice.append(aula[0])
                    advice.append([str(int(hStart))+':'+str(int(hStart*60%60)), str(int(hFin))+':'+str(int(hFin*60%60)), hFin-hStart])
                hStart = hFin+0.25
                hFin = hStart
                wasFree = 0
        if len(advice)!=0 :
            advices.append(advice);
    for advice in advices:
        print(advice)

getAdvice("MIA", 18, 11, 2021, 4)
