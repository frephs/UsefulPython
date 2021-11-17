import requests
from bs4 import BeautifulSoup

def getUrl(ed,gg, mm, yy):
    return "https://www7.ceda.polimi.it/spazi/spazi/controller/OccupazioniGiornoEsatto.do?csic="+str(ed)+"&categoria=tutte&tipologia=tutte&giorno_day="+str(gg)+"&giorno_month="+str(mm)+"&giorno_year="+str(yy)+"&jaf_giorno_date_format=dd%2FMM%2Fyyyy&evn_visualizza="

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
        advices.sort(key=returnHours, reverse=True)
    for advice in advices:
        print(advice)

def returnHours(elem):
    return elem[1][2]

def output():
    from datetime import date
    t = date.today()
    print("\n--------\nTODAY\n---------")
    getAdvice("MIA", t.day, t.month, t.year, 3)
    print("\n--------\nTOMORROW\n---------")
    getAdvice("MIA", t.day+1, t.month, t.year, 3)

output()

#FOR REFERENCE
edifici = [
["COE", "Como"],
["COE04", "Como - Via Anzani"],
["COE02", "Como - Via Castelnuovo"],
["COE03", "Como - Via Valleggio"],
["COE08", "Como - Via Zezio"],
["CRG", "Cremona"],
["CRG01", "Cremona - Via Sesto"],
["LCF", "Lecco"],
["LCF04", "Lecco - Via Ghislanzoni"],
["MNI", "Mantova"],
["MNI01", "Mantova - Via Scarsellini 15"],
["MNI02", "Mantova - Via Scarsellini 2"],
["MIB", "Milano Bovisa"],
["MIB02", "Milano Bovisa - Via Durando"],
["MIB01", "Milano Bovisa - Via La Masa"],
["MIA", "Milano Città Studi"],
["MIA11", "Milano Città Studi - Piazza Leonardo da Vinci 26"],
["MIA01", "Milano Città Studi - Piazza Leonardo da Vinci 32"],
["MIA03", "Milano Città Studi - Via Bassini"],
["MIA02", "Milano Città Studi - Via Bonardi"],
["MIA06", "Milano Città Studi - Via Colombo 40"],
["MIA07", "Milano Città Studi - Via Colombo 81"],
["MIA14", "Milano Città Studi - Via Golgi 20"],
["MIA04", "Milano Città Studi - Via Golgi 40"],
["MIA05", "Milano Città Studi - Via Mancinelli"],
["MIA15", "Milano Città Studi - Via Pascoli 70"],
["MIA09", "Milano Città Studi - Viale Romagna"],
["PCL", "Piacenza"],
["PCL04", "Piacenza - Via Scalabrini 113"],
["PCL01", "Piacenza - Via Scalabrini 76"]]
