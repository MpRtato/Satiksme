import requests
import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
#options.binary_location = "\chrome.exe" #SKOLAS DATORU PATCH
options.headless = True
driver = uc.Chrome(use_subprocess=True,options=options)

transp = requests.get('https://www.rigassatiksme.lv/lv/').text
transpS = BS(transp, 'lxml')

# Transportlīdz
# Tramvajs
tramvajs = []
trams = transpS.find('div', id='transportType-tram')
tram = trams.select('li.item ')
i = 0
for j in tram:
    tramnr = tram[i].text.split()
    tramvajs.extend(tramnr)
    i = i + 1
# Trolejbuss
trolejbuss = []
trols = transpS.find('div', id='transportType-trolley')
trol = trols.select('li.item ')
i = 0
for j in trol:
    trolnr = trol[i].text.split()
    trolejbuss.extend(trolnr)
    i = i + 1
# Autobuss
autobuss = []
autos = transpS.find('div', id='transportType-bus')
auto = autos.select('li.item ')
i = 0
for j in auto:
    autonr = auto[i].text.split()
    autobuss.extend(autonr)
    i = i + 1
# Ekspressbuss
ekspressbuss = []
eksps = transpS.find('div', id='transportType-express')
eksp = eksps.select('li.item ')
i = 0
for j in eksp:
    ekspnr = eksp[i].text.split()
    ekspressbuss.extend(ekspnr)
    i = i + 1

# Ievade
# Transportlīdzeklim
print('Transportlīdzekļa vieds: ')
print('Tramvajs(1)')
print('Trolejbuss(2)')
print('Autobuss(3)')
print('Ekspressbuss(4)')

while 1 < 2:
    Transports = input('>')

    if Transports == '1':
        transpn = tramvajs
        transpv = 'Tramvajs'
        mtranspv = 'tram'
        break

    elif Transports == '2':
        transpn = trolejbuss
        transpv = 'Trolejbuss'
        mtranspv = 'trol'
        break

    elif Transports == '3':
        transpn = autobuss
        transpv = 'Autobuss'
        mtranspv = 'bus'
        break

    elif Transports == '4':
        transpn = ekspressbuss
        transpv = 'Ekspressbuss'
        mtranspv = 'expressbus'
        break

    else:
        print('')
        print('Nepareizs skaitlis!')

# Nummuram
print('')
print('Transportlidzekļa nummurs: ')
print(transpn)
while 1 < 2:
    Nummurs = input('>')
    if Nummurs in transpn:
        break

    else:
        print('')
        print('Nav tāds ' + transpv + '!')

# Saraksts
# dabusana
links = 'https://saraksti.rigassatiksme.lv/index.html#' + mtranspv + '/' + Nummurs + '/a-b'

while(1<2):
    tags = []
    vietas = []
    tgtv = 0
    iepv = []
    rest=0

    while rest==0:
        driver.get(links)
        driver.implicitly_wait(20)
        time.sleep(2)
        jslinks=driver.page_source

        saraksts = BS(jslinks, "lxml")
        pieturas = saraksts.select("a.hover")

        i = 0
        for j in pieturas:
            if i == 0 and 'UAB „Merakas“' not in pieturas[i].text:
                i = i + 1

            elif i == 0 and 'UAB „Merakas“' in pieturas[i].text:
                i = i + 1

            else:
                iepv.append(tgtv)
                tgtv = pieturas[i].text

                if tgtv in iepv:
                    break

                else:
                    vietas.append(pieturas[i].text)

                i = i + 1
        rest=len(vietas)

    #salidzinasana pec kartas(No kurienes uz kurieni)
    transpvr = list(transpv)
    transpvr.pop(-1)
    transpvr.append('am')
    transpvr = ''.join(transpvr)

    #ievade no
    print('')
    print('NO: ')

    i=0
    for j in vietas:
        print(vietas[i]+'({})'.format(i+1))
        i=i+1

    vietano=0
    j=1
    while(j<2):
        no = input('>')

        if no.isdigit() == False:
            no=99999

        i=0
        while i<len(vietas):
            if int(no)-1 == vietas.index(vietas[i]):
                vietano=vietas[i]
                vietanonr=vietas.index(vietas[i])
                j=3

            if vietano==0 and len(vietas)==i+1:
                print('')
                print(Nummurs+'. '+transpvr+' nav tādas peituras!')

            i = i + 1

    #ievade uz
    print('')
    print('UZ: ')

    i=0
    for j in vietas:
        print(vietas[i]+'({})'.format(i+1))
        i=i+1

    vietauz=0
    j=1
    while(j<2):
        uz = input('>')

        if uz.isdigit() == False:
            uz=99999

        i=0
        while i<len(vietas):
            if int(uz)-1 == vietas.index(vietas[i]):
                vietauz=vietas[i]
                vietauznr=vietas.index(vietas[i])
                j=3

            if vietauz==0 and len(vietas)==i+1:
                print('')
                print(Nummurs+'. '+transpvr+' nav tādas peituras!')

            i = i + 1

    vietanoo = driver.find_element(By.XPATH, '//*[@id="dlDirStops1"]/dt[{}]/a'.format(no)).text
    vietauzz = driver.find_element(By.XPATH, '//*[@id="dlDirStops1"]/dt[{}]/a'.format(uz)).text

    #virziena ieguve
    if vietanonr<vietauznr:
        virziens='a-b'

    elif vietanonr>vietauznr:
        virziens='b-a'

    linksl='https://saraksti.rigassatiksme.lv/index.html#' + mtranspv + '/' + Nummurs + '/'+virziens

    driver.get(linksl)
    driver.implicitly_wait(20)

    #vietas izmantosana
    time.sleep(2)

    sarakstavietas=driver.find_element(By.XPATH,'//*[@id="dlDirStops1"]').text
    sarakstavietas=sarakstavietas.splitlines()
    if vietanoo and vietauzz in sarakstavietas:
        break

    else:
        print('')
        print(Nummurs + '. ' + transpv + ' nebrauc no pieturas ' + vietanoo + ' uz pieturu ' + vietauzz)

no=sarakstavietas.index(vietanoo)+1
uz=sarakstavietas.index(vietauzz)+1

vietasar=driver.find_element(By.XPATH,'//*[@id="dlDirStops1"]/dt[{}]'.format(uz))
driver.implicitly_wait(10)
vietasar.click()

#darba diena vai brīvdiena
print('')
print('Saraksta veids:')
print('Darba dienu(1)')
if transpv != 'Ekspressbuss':
    print('Brīvdienu(2)')

while 1<2:
    diena=input('>')
    if transpv != 'Ekspressbuss':
        if diena == '1' or diena == '2':
            if diena == '1':
                diena ='darba'
                break

            elif diena == '2':
                diena='briva'
                break

        else:
            print('')
            print('Nav tāda saraksta veida!')

    else:
        if diena == '1':
            diena = 'darba'
            break

        else:
            print('')
            print('Nav tāda saraksta veida!')

#pirmais un pedejais laiks
minlaiks=0
maxlaiks=0

def minmaxlaiks(dlaiki): #iegust transporta minimalo un maximalo laiku atkariba no argumenta
    global maxlaiks
    global minlaiks
    dlaiki=dlaiki.splitlines()

    j = 0
    while j > -2:
        plaiki=list(dlaiki[j])
        if plaiki[0].isdigit()==False:
            while plaiki[0].isdigit()==False:
                plaiki.pop(0)
        plaiki = ''.join(plaiki)
        mlaiki = plaiki.split(' ')
        llaiks = mlaiki[0]
        mlaiki.pop(0)
        mlaiki = list(mlaiki[0])

        mlaikif = []
        l = 0
        i = 0
        ii = 1
        while l < len(mlaiki) / 2:
            num = mlaiki[i] + mlaiki[ii]
            mlaikif.append(num)
            i = i + 2
            ii = ii + 2
            l = l + 1

        if j == -1:
            maxlaiks = llaiks + ':' + mlaikif[-1]

        else:
            minlaiks = llaiks + ':' + mlaikif[0]

        j = j - 1

if diena == 'darba':
    dienlaiki=driver.find_element(By.XPATH,'//*[@id="divScheduleContentInner"]/table[1]/tbody[2]').text
    minmaxlaiks(dienlaiki)
    dienasv=1

if diena=='briva':
    dienlaiki = driver.find_element(By.XPATH, '//*[@id="divScheduleContentInner"]/table[2]/tbody[2]').text
    minmaxlaiks(dienlaiki)
    dienasv = 2

#minimalais laiks
minlaiks01=minlaiks.split(':')

#maksimalais laiks
maxlaiks01=maxlaiks.split(':')


#laika ievade un pārbaude
print('')
print('Laiks: (hh:mm / hh mm / hhmm)')

laiks=0
while laiks==0:
    laiksi=input('>')

    laiksparb=(list(laiksi))
    if len(laiksparb) <4 or len(laiksparb)>5:
        print('')
        print('Nepareiza sintakse!')

    elif len(laiksparb)==4:

        if laiksparb[0].isdigit() == False or laiksparb[1].isdigit() == False or laiksparb[2].isdigit() == False or laiksparb[3].isdigit() == False:
            print('')
            print('Nepareiza sintakse!')

        elif int(laiksparb[0])<0 or int(laiksparb[0])>2:
            print('')
            print('Dienā ir 24 stundas!')

        elif int(laiksparb[1])<0:
            print('')
            print('Dienā ir 24 stundas!')

        elif int(laiksparb[0])<2:
            if int(laiksparb[1])<0 or int(laiksparb[1])>9:
                print('')
                print('Dienā ir 24 stundas!')
            elif int(laiksparb[2]) < 0 or int(laiksparb[2]) > 5:
                print('')
                print('Stundā ir 60 minūtes!')

            elif int(laiksparb[3]) < 0 or int(laiksparb[3]) > 9:
                print('')
                print('Stundā ir 60 minūtes!')

            else:
                laikssadal = list(laiksi)
                if laikssadal[0] == '0':
                    if int(laikssadal[1]) < int(minlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) < int(
                            minlaiks01[1]) and int(laikssadal[1])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[1]) < int(minlaiks01[0]) and int(laikssadal[1])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[1]) == int(minlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) < int(
                            minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[1]) > int(maxlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) > int(
                            maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!a')

                    elif int(laikssadal[1]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!b')

                    elif int(laikssadal[1]) == int(maxlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) > int(
                            maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!c')

                    else:
                        laiks = laikssadal[1] + ':' + laikssadal[2] + laikssadal[3]

                else:
                    if int(laikssadal[0] + laikssadal[1]) < int(minlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) < int(minlaiks01[0]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) == int(minlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) > int(maxlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) > int(maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) == int(maxlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) > int(maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    else:
                        laiks = laikssadal[0] + laikssadal[1] + ':' + laikssadal[2] + laikssadal[3]


        elif int(laiksparb[0])==2:
            if int(laiksparb[1])<0 or int(laiksparb[1])>3:
                print('')
                print('Dienā ir 24 stundas!')
            elif int(laiksparb[2]) < 0 or int(laiksparb[2]) > 5:
                print('')
                print('Stundā ir 60 minūtes!')

            elif int(laiksparb[3]) < 0 or int(laiksparb[3]) > 9:
                print('')
                print('Stundā ir 60 minūtes!')

            else:
                laikssadal = list(laiksi)
                if laikssadal[0] == '0':
                    if int(laikssadal[1]) < int(minlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) < int(
                            minlaiks01[1]) and int(laikssadal[1])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[1]) < int(minlaiks01[0]) and int(laikssadal[1])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[1]) == int(minlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) < int(
                            minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[1]) > int(maxlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) > int(
                            maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    elif int(laikssadal[1]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    elif int(laikssadal[1]) == int(maxlaiks01[0]) and int(laikssadal[2] + laikssadal[3]) > int(
                            maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    else:
                        laiks = laikssadal[1] + ':' + laikssadal[2] + laikssadal[3]

                else:
                    if int(laikssadal[0] + laikssadal[1]) < int(minlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) < int(minlaiks01[0]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) == int(minlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) > int(maxlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) > int(maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    elif int(laikssadal[0] + laikssadal[1]) == int(maxlaiks01[0]) and int(
                            laikssadal[2] + laikssadal[3]) > int(maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')

                    else:
                        laiks = laikssadal[0] + laikssadal[1] + ':' + laikssadal[2] + laikssadal[3]

    elif laiksparb[0].isdigit() == False or laiksparb[1].isdigit() == False or laiksparb[3].isdigit() == False or laiksparb[4].isdigit() == False:
        print('')
        print('Nepareiza sintakse!')

    elif int(laiksparb[0]) < 0 or int(laiksparb[0]) > 2:
        print('')
        print('Dienā ir 24 stundas!')

    elif int(laiksparb[1]) < 0:
        print('')
        print('Dienā ir 24 stundas!')

    elif int(laiksparb[0]) < 2:
        if int(laiksparb[1]) < 0 or int(laiksparb[1]) > 9:
            print('')
            print('Dienā ir 24 stundas!')
        elif int(laiksparb[3]) < 0 or int(laiksparb[3]) > 5:
            print('')
            print('Stundā ir 60 minūtes!')

        elif int(laiksparb[4]) < 0 or int(laiksparb[4]) > 9:
            print('')
            print('Stundā ir 60 minūtes!')

        else:

            i = 0
            if ':' in laiksparb[2]:
                laiks = laiksi.split(':')
                laikshh = list(laiks[0])
                i = 1

            elif ' ' in laiksparb[2]:
                laiks = laiksi.split()
                laikshh = list(laiks[0])
                i = 1

            else:
                print('')
                print('Nepareiza sintakse!')

            if i == 1:
                if '0' in laikshh[0]:
                    laikshh.pop(0)
                    laiks.pop(0)
                    if int(laikshh[0]) < int(minlaiks01[0]) and int(laiks[0]) < int(minlaiks01[1]) and int(laikshh[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) < int(minlaiks01[0]) and int(laikshh[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) == int(minlaiks01[0]) and int(laiks[0]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) > int(maxlaiks01[0]) and int(laiks[0]) > int(maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) == int(maxlaiks01[0]) and int(laiks[0]) > int(maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    else:
                        laikshh.extend(laiks)
                        laiks = ':'.join(laikshh)

                else:
                    if int(laiks[0]+laiks[1]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) < int(minlaiks01[0]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) == int(minlaiks01[0]) and int(laiks[1]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) > int(maxlaiks01[0]) and int(laiks[1]) > int(maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) == int(maxlaiks01[0]) and int(laiks[1]) > int(maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    else:
                        laiks = ':'.join(laiks)

    elif int(laiksparb[0]) == 2:
        if int(laiksparb[1]) < 0 or int(laiksparb[1]) > 3:
            print('')
            print('Dienā ir 24 stundas!')
        elif int(laiksparb[3]) < 0 or int(laiksparb[3]) > 5:
            print('')
            print('Stundā ir 60 minūtes!')

        elif int(laiksparb[4]) < 0 or int(laiksparb[4]) > 9:
            print('')
            print('Stundā ir 60 minūtes!')

        else:

            i = 0
            if ':' in laiksparb[2]:
                laiks = laiksi.split(':')
                laikshh = list(laiks[0])
                i = 1

            elif ' ' in laiksparb[2]:
                laiks = laiksi.split()
                laikshh = list(laiks[0])
                i = 1

            else:
                print('')
                print('Nepareiza sintakse!')

            if i == 1:
                if '0' in laikshh[0]:
                    laikshh.pop(0)
                    laiks.pop(0)
                    if int(laikshh[0]) < int(minlaiks01[0]) and int(laiks[0]) < int(minlaiks01[1]) and int(laikshh[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) < int(minlaiks01[0]) and int(laikshh[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) == int(minlaiks01[0]) and int(laiks[0]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) > int(maxlaiks01[0]) and int(laiks[0]) > int(maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laikshh[0]) == int(maxlaiks01[0]) and int(laiks[0]) > int(maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    else:
                        laikshh.extend(laiks)
                        laiks = ':'.join(laikshh)

                else:
                    if int(laiks[0]+laiks[1]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) < int(minlaiks01[0]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) == int(minlaiks01[0]) and int(laiks[1]) < int(minlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pirmais attiešanas laiks: ' + minlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) > int(maxlaiks01[0]) and int(laiks[1]) > int(maxlaiks01[1]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) > int(maxlaiks01[0]) and int(maxlaiks01[0])!=0:
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    elif int(laiks[0]) == int(maxlaiks01[0]) and int(laiks[1]) > int(maxlaiks01[1]):
                        print('')
                        print(Nummurs+'. '+transpvr+' pēdējais attiešanas laiks: ' + maxlaiks + '!')
                        laiks = 0

                    else:
                        laiks = ':'.join(laiks)

#visu laiku iegusana
dienlaiki=dienlaiki.splitlines()

visslaiki=[]

i=0
while i<len(dienlaiki):
    dienlaiks=dienlaiki[i].split(' ')
    if dienlaiks[0] == '':
        while dienlaiks[0].isdigit()==False:
            dienlaiks.pop(0)

    if dienlaiks[0].isdigit() == True:
        stunda = dienlaiks[0]
        minutes=list(dienlaiks[1])

        l=0
        j=0
        jj=1
        while l<len(minutes)/2:
            minute=minutes[j]+minutes[jj]
            visslaiki.append(stunda+':'+minute)

            j=j+2
            jj=jj+2
            l=l+1


    i=i+1

#Laiku salidzinasana
parvl=0
def lminutes(pl): #parveido laiku no stundam un minutem uz minutem
    global parvl

    pl=pl.split(':')
    if pl[0]=='0':
        hmin=24*60

    else:
        hmin=int(pl[0])*60

    parvl=hmin+int(pl[1])

lminutes(laiks)
ievadl=parvl

iepl=0

j=0
i=-1
ii=0
iii=1
while 1<2:
    if j>0:
        lminutes(visslaiki[i])
        iepl=parvl

    lminutes(visslaiki[ii])
    tgtl=parvl

    if iii>=len(visslaiki):
        nakl=0

    else:
        lminutes(visslaiki[iii])
        nakl=parvl

    tgtst=tgtl-ievadl
    tgtst=abs(tgtst)

    iepst=iepl-ievadl
    iepst=abs(iepst)

    nakst=nakl-ievadl
    nakst=abs(nakst)

    if iepst<nakst and iepst<tgtst:
        salidzlaiks=visslaiki[i]
        break

    if iii >= len(visslaiki):
        salidzlaiks = visslaiki[ii]
        break



    j=j+1
    i=i+1
    ii=ii+1
    iii=iii+1

#laika izvele
salidzdalas=salidzlaiks.split(':')
salidzliel=salidzdalas[0]
salidzmaz=salidzdalas[1]

lieliedalas=[]
mazdalas=[]

i=0
while i<len(dienlaiki):
    dienlaiks=dienlaiki[i].split(' ')
    if dienlaiks[0] == '':
        while dienlaiks[0].isdigit()==False:
            dienlaiks.pop(0)

    lileiedala = dienlaiks[0]
    lieliedalas.append(lileiedala)

    i=i+1

indeks=lieliedalas.index(salidzliel)+1

lielsatiksme=driver.find_element(By.XPATH,'//*[@id="divScheduleContentInner"]/table['+str(dienasv)+']/tbody[2]/tr['+str(indeks)+']/td').text
lielsatiksme=list(lielsatiksme)

l=0
j=0
jj=1
while l<len(lielsatiksme)/2:
    mazsatiksme=lielsatiksme[j]+lielsatiksme[jj]
    mazdalas.append(mazsatiksme)

    j=j+2
    jj=jj+2
    l=l+1

mazindeks=mazdalas.index(salidzmaz)+1

mazsatiksme=driver.find_element(By.XPATH,'//*[@id="divScheduleContentInner"]/table['+str(dienasv)+']/tbody[2]/tr['+str(indeks)+']/td/a['+str(mazindeks)+']')
mazsatiksme.click()

iedalas=driver.iekaplaiks=driver.find_element(By.XPATH,'//*[@id="dlDirStops1"]').text
driver.implicitly_wait(10)
iedalas=iedalas.splitlines()

i=0
while i<len(iedalas):
    iedala=iedalas[i].split(' ')
    iedala.pop(0)
    iedala.pop(0)
    iedala=' '.join(iedala)
    if vietanoo == iedala:
        vietasindeks=i+1
        break

    i=i+1

iekaplaiks=driver.find_element(By.XPATH,'//*[@id="dlDirStops1"]/dt[{}]/a/b'.format(vietasindeks)).text

#izvade
print('')
print('')
print('#Transportlīdzeklis: '+Nummurs+'. '+transpv)
print('#Brauc no pieturas '+vietanoo+' līdz pieturai '+vietauzz)
print('#Pieturā '+vietauzz+' ierodas: '+salidzlaiks)
print('#No pieturas '+vietanoo+' attiet: '+iekaplaiks)
print('')
print('#Ievadītais laiks: '+laiks)
print('')