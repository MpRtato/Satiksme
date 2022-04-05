import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.headless = False
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
        print('Nepareizs skaitlis!')

# Nummuram
print('Transportlidzekļa nummurs: ')
print(transpn)
while 1 < 2:
    Nummurs = input('>')
    if Nummurs in transpn:
        break

    else:
        print('Nav tāds ' + transpv + '!')

# Saraksts
# dabusana
links = 'https://saraksti.rigassatiksme.lv/index.html#' + mtranspv + '/' + Nummurs + '/a-b'

tags = []
vietas = []
tgtv = 0
iepv = []

driver.get(links)
driver.implicitly_wait(10)
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

#salidzinasana pec kartas(No kurienes uz kurieni)
#ievade no
print('NO: ')

i=0
for j in vietas:
    print(vietas[i]+'({})'.format(i+1))
    i=i+1

vietano=0
j=1
while(j<2):
    no = input('>')
    i=0

    while i<len(vietas):
        if int(no)-1 == vietas.index(vietas[i]):
            vietano=vietas[i]
            vietanonr=vietas.index(vietas[i])
            j=3

        if vietano==0 and len(vietas)==i+1:
            transpvr = list(transpv)
            transpvr.pop(-1)
            transpvr.append('am')
            transpvr = ''.join(transpvr)
            print(Nummurs+'. '+transpvr+' nav tādas peituras!')

        i = i + 1

#ievade uz
print('UZ: ')

i=0
for j in vietas:
    print(vietas[i]+'({})'.format(i+1))
    i=i+1

vietauz=0
j=1
while(j<2):
    uz = input('>')
    i=0

    while i<len(vietas):
        if int(uz)-1 == vietas.index(vietas[i]):
            vietauz=vietas[i]
            vietauznr=vietas.index(vietas[i])
            j=3

        if vietauz==0 and len(vietas)==i+1:
            transpvr = list(transpv)
            transpvr.pop(-1)
            transpvr.append('am')
            transpvr = ''.join(transpvr)
            print(Nummurs+'. '+transpvr+' nav tādas peituras!')

        i = i + 1

#virziena ieguve
if vietanonr<vietauznr:
    virziens='a-b'

elif vietanonr>vietauznr:
    virziens='b-a'

linksl='https://saraksti.rigassatiksme.lv/index.html#' + mtranspv + '/' + Nummurs + '/'+virziens

#darba diena vai brīvdiena
print('Saraksta veids:')
print('Darba dienu(1)')
print('Brīvdienu(2)')

diena=input('>')
if diena == '1' or diena == '2':
    if diena == '1':
        diena ='darba'

    elif diena == '2':
        diena='briva'

else:
    print('Nav tāda saraksta veida!')

#laika ievade un pārbaude
#session = HTMLSession()
#jslinksl = session.get(linksl)

#izm=0
#while izm == 0:
    #print('...')
    #jslinksl.html.render(timeout=10, sleep=1)

    #laiki = BS(jslinksl.html.html, "lxml")
    #pirmlaiks = laiki.select("a.hover")
    #izm = len(pirmlaiks)

#print(pirmlaiks)

print('Laiks: (hh:mm / hh mm / hhmm)')

laiks=0
while laiks==0:
    laiksi=input('>')

    laiksparb=(list(laiksi))
    if len(laiksparb) <4 or len(laiksparb)>5:
        print('Nepareiza sintakse!')

    elif len(laiksparb)==4:
        if laiksparb[0].isdigit() == False or laiksparb[1].isdigit() == False or laiksparb[2].isdigit() == False or laiksparb[3].isdigit() == False:
            print('Nepareiza sintakse!')

        else:
            laikssadal=list(laiksi)
            if laikssadal[0]=='0':
                if int(laikssadal[1])<5:
                    print('pirmais attiesanas laiks')

                else:
                    laiks= laikssadal[1]+':'+laikssadal[2]+laikssadal[3]

            else:
                laiks = laikssadal[0] + laikssadal[1] + ':' + laikssadal[2] + laikssadal[3]



    elif laiksparb[0].isdigit() == False or laiksparb[1].isdigit() == False or laiksparb[3].isdigit() == False or laiksparb[4].isdigit() == False:
        print('Nepareiza sintakse!')

    else:

        i=0
        if ':' in laiksparb[2]:
            laiks=laiksi.split(':')
            laikshh = list(laiks[0])
            i=1

        elif ' ' in laiksparb[2]:
            laiks=laiksi.split()
            laikshh = list(laiks[0])
            i=1

        else:
            print('Nepareiza sintakse!')

        if i==1:
            if '0' not in laikshh[0]:
                laiks=':'.join(laiks)

            elif '0' in laikshh[0]:
                laikshh.pop(0)
                laiks.pop(0)
                laikshh.extend(laiks)
                laiks = ':'.join(laikshh)

print(laiks)