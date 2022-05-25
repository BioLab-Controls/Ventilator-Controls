import csv  

pres = []
t = []

def updatePres(pdata,tdata):
    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

    pres.append(pdata)
    t.append(tdata)
    writer.writerow()
    writer.writerow(tdata)

def updateFile(pdata,tdata):
    updatePres(pdata,tdata)

