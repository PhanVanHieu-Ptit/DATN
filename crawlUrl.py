import os

import requests
from bs4 import BeautifulSoup
import csv


host = 'https://vbpl.vn'
endPoint = '/TW/Pages/vanban.aspx?dvid=13'
ids = [18,20,21,22]
# limits = [124,442,1302,1355]
nameDocList = ['nghiQuyet.csv','nghiDinh.csv','quyetDinh.csv','thongTu.csv']
nameFolderRoot = 'url_doc'
limit = 124

def crawl_url(numDocList):
    docs = []
    i = 1

    while True:
        print('Doc ',str(i)+'.')
        current_url = host + endPoint + '&idLoaiVanBan=' + str(ids[numDocList]) + '&Page='+ str(i)
        print('Downloading from  ', current_url +' ............')

        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, "html.parser")
        link_elements = soup.select("a[href]")

        urlDownLoad = []
        for link_element in link_elements:
            url = link_element["href"]
            if "javascript:downloadfile" in url:
                urlDownLoad.append(url)


        for url in urlDownLoad:
            urlTemp = url[url.index("('")+1 :url.index("')")]
            urlTemp = urlTemp.replace("'", "")
            urlTemp = urlTemp.split(',')

            if  urlTemp[0].lower().endswith('.doc') or urlTemp[0].lower().endswith('.docx'):
                doc = {"name": urlTemp[0], "url": host + urlTemp[1]}
                docs.append(doc)

        print('=======================================')
        print(nameDocList[numDocList]+' : '+ str(len(docs)) +' rows')
        print('=======================================')

        print('--- Start write into file CSV ---')
        print('Write file ',nameDocList[numDocList])
        write_into_file(nameDocList[numDocList], docs)
        print('--- Done write file! ---')
        if i == limit: break
        i = i + 1


def write_into_file(nameFile, docs):
    print('docs: ',docs)
    with open(os.path.join(nameFolderRoot,nameFile), 'w', encoding='UTF-8',newline='') as csv_file:
        writer = csv.writer(csv_file)

        # name,url
        for doc in docs:
            writer.writerow(doc.values())



def crawl_url_from_web():
    print('============================== START CRAWL! =================================')

    if not os.path.exists(nameFolderRoot):
        print('Create folder ', nameFolderRoot)
        os.mkdir(nameFolderRoot)

    for i in range(4):
        print('\n************************* '+nameDocList[i][:len(nameDocList[i])-4].upper()+' ***********************')
        crawl_url(i)
    print('============================== DONE CRAWL! =================================')

if __name__ == '__main__':
    print('===================== START! ============================')
    crawl_url_from_web()
    print('===================== END! ============================')