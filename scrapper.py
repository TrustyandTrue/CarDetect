from bs4 import BeautifulSoup
import urllib2
import shutil
import requests
from urlparse import urljoin
import time
import os
import re
import getpass
import uuid

#, 'VW': 74, 'AUDI': 9, 'OPEL': 54, 'BENZ': 47, 'SEAT': 64
brands = {'BMW': 13, 'VW': 74, 'AUDI': 9, 'OPEL': 54, 'BENZ': 47, 'SEAT': 64}

vwModels = {'Beetle Neu': 15381, 'Golf': 2084, 'Golf Cabriolet': 20341,
            'Golf GTI': 20342, 'Golf Plus': 20026, 'Golf Sportsvan': 20376, 'Golf Variant': 20340, 'Passat': 2089, 'Passat2': 20339, 'Passat3': 20337, 'Passat4': 20338, 'Polo': 2090, 'Polo Cross': 20170, 'Polo GTI': 20335, 'Sharan': 2093, 'Tiguan': 19063}

bmwModels = {'1er':-37 , 'z':-45, '3er':-38, '4er': -97, '6er': -40, '7er': -41, '5er': -39, 'M': -43}

benzModels = {'a180': 18486, 'a190': 15703, 'c300': 19249, 'c280': 2099, 'c400': 20916, 'cl': -59, 'g': -62, 's': -66, 'sl': -67, 'slk': -68}

opelModels = {'adam': 20191, 'corsa': 1918, 'insignia': 19101, 'zafira': 15660, 'omega': 1924}

audiModels = {'A1': 19083, 'A2': 16416, 'A3': 1624, 'A4': 1626, 'TT': 15627, 'TT RS': 20056, 'Q2': 74373, 'Q3': 19715, 'Q5': 19155, 'Q7': 18683, 'S1': 20369}

skodaModels = {'Fabia': 15878, 'Superb': 16621, '120': 18120, '130': 18130, 'Pick-up': 18140, 'Favorit': 2014, 'Felicia': 2015, 'Forman': 2016, 'Octavia': 15222, '105': 18642, '130': 18643, 'Roomster': 18877}

def getUserName():
    user = getpass.getuser()
    print(user)
    return user

def checkDirExists(folder):
    path = os.path.exists("/Users/" + getUserName() + "/Documents/" + folder)

    if path:
        return folder
    else:
        print("directory " + folder + " not found, create directory now....")
        os.makedirs("/Users/"+ getUserName() + "/Documents/" + folder)
        print("directory " + folder + " created")
        return folder


myPath = "/Users/"+ getUserName() + "/Documents/" + checkDirExists("Dataset/")

def remove_suffix(text):
    a = text.split("?")[0]
    return a

def make_soup(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    html = urllib2.urlopen(req)
    return BeautifulSoup(html, 'html.parser')

def get_images(url, brand, getAll):
    print(url)
    soup = make_soup(url)
    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + " images found.")
    print('Downloading images to current working directory.')
    image_links = [each.get('src') for each in images]
    if getAll:
        image_links += [each.get('data-src') for each in images]
    image_links = filter(None, image_links)
    for each in image_links:
        try:
            each = re.sub('420x315', '640x480', each)
            print('image link: ' + each)
            filename = each.strip().split('/')[-2].strip()
            print('filename:' +filename)
            new_filename = remove_suffix(filename)
            print('new_filename:' +new_filename)
            src = urljoin(url, each)
            response = requests.get(src, stream=True)
            fullfilename = os.path.join(myPath + brand, new_filename)
            print('fullfilename - '+fullfilename)
            if not os.path.exists(fullfilename):
                with open(fullfilename, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                    print('Getting: ' + filename)
        except:
            print('An error occured. Continuing.')
    print('Done.')


def scrap_brand_pages(count):
    for name, id in brands.items():
        checkDirExists("Dataset/" + name)
        print ("get images for " + name)
        for x in range(1, count + 1):
            get_images(
                'https://www.autoscout24.de/ergebnisse?powertype=kw&custtype=P&pricetype=public&cy=D&mmvmk0=' + str(id) + '&mmvco=1&pricefrom=5000&sort=standard&ustate=N&ustate=U&atype=C&page=' +
                str(x) + '&size=20', name, False)


def scrap_models(modelDict, brand):

    for name, id in modelDict.items():
        print(name)
        print(brand)
        checkDirExists("Dataset/" + name)
        for x in range(1, 21):
            get_images(
                'https://www.autoscout24.de/ergebnisse?powertype=kw&custtype=P&pricetype=public&cy=D&mmvmk0=' + str(brand) + '&mmvco=1&pricefrom=5000&sort=standard&ustate=N&ustate=U&atype=C&page=' + (str(x)) + '&size=20&mmvmd0=' + str(id), name, False)

def scrap_models_to_brand(modelDict, brand, brandname):

    for name, id in modelDict.items():
        print(name)
        print(brand)
        checkDirExists("Dataset/" + name)
        for x in range(1, 20):
            get_images(
                'https://www.autoscout24.de/ergebnisse?powertype=kw&custtype=P&pricetype=public&cy=D&mmvmk0=' + str(brand) + '&mmvco=1&pricefrom=5000&sort=standard&ustate=N&ustate=U&atype=C&page=' + (str(x)) + '&size=20&mmvmd0=' + str(id), name, False)


#scrap_brand_pages(1)
#scrap_models_to_brand(vwModels, 74, 'VW')
#scrap_models_to_brand(bmwModels, 13, 'BMW')
scrap_models_to_brand(benzModels, 47, 'BENZ')
scrap_models_to_brand(opelModels, 54, 'OPEL')
scrap_models_to_brand(skodaModels, 65, 'SKODA')
scrap_models_to_brand(audiModels, 9, 'AUDI')
