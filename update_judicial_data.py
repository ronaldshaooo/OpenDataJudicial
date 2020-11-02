from bs4 import BeautifulSoup
import os
import patoolib
import requests
import shutil  

judicial_history_directory = 'judicial_history'
fincial_judgement_directory = 'fincial_judgement'

def copy_fincial_judgement():
    for root, _dirs, files in os.walk(judicial_history_directory):
        for item in files:
            if '金' in item:
                shutil.copy(os.sep.join([root, item]), fincial_judgement_directory)

def check_history(link):
    file_dir = link.replace('rar/','').replace('.rar','')
    if os.path.isdir('judicial_history/{}'.format(file_dir)):
        print('{} exists'.format(file_dir))
    else:
        download_link = 'http://data.judicial.gov.tw/{}'.format(link)
        print(download_link)
        with open('file.rar', "wb") as file:
            response = requests.get(download_link)
            file.write(response.content)
        patoolib.extract_archive('file.rar', outdir= '{}/{}'.format(judicial_history_directory, file_dir))

def refresh():
    if not os.path.isdir(judicial_history_directory):
        os.mkdir(judicial_history_directory)
    if not os.path.isdir(fincial_judgement_directory):
        os.mkdir(fincial_judgement_directory)

    response = requests.get("http://data.judicial.gov.tw/")
    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.find_all('a', href=True):
        link = item['href']
        check_history(link)



