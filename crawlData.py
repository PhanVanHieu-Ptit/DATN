from datetime import datetime
import os

import requests
import csv

import aspose.words as aw

nameFolderRoot = 'doc'
nameFolderConvertRoot = 'convert'
nameFolderDeleteRoot = 'deleted'
folderName = ['nghiDinh', 'nghiQuyet', 'quyetDinh', 'thongTu']
containSuitNameFileList = [['nd.cp','nd_cp','nd-cp', 'nđ.cp', 'nđ-cp','nđ_cp'],['.'],['.'],['.']]
containNoSuitNameFileList = [['phụ lục','phu luc'],['phu luc','phuluc','qđ','mẫu','phucap','tt','chuongtrinh','bieuthue'],[],[]]

def read_file(fileNameRead):
    with open(fileNameRead, encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            data.append({'name': row[0], 'url': row[1]})
        return data

def download_file(filename, url):
    # global req
    try:
        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None


def crawl_data():
    print('======================================Start download file!==============================================================')


    if not os.path.exists(nameFolderRoot):
        print('*** Create folder '+nameFolderRoot)
        os.mkdir(nameFolderRoot)

    for i in range(0,len(folderName)):

        print('=========================== ' + folderName[i].upper() + ' ======================================')

        if not os.path.exists(os.path.join(nameFolderRoot, folderName[i])):
            # create forder
            print('*** Create folder '+ nameFolderRoot +'/'+folderName[i])
            os.mkdir(os.path.join(nameFolderRoot, folderName[i]))

        # read urls from file
        print('--- Start read ---')
        print('Read name url of file ', folderName[i] + '.csv')
        nameUrlList = read_file(os.path.join('url', folderName[i] + '.csv'))
        print('Len: ', str(len(folderName[i])) + 'docs')
        print('--- Done read ---')

        print('--- Start download ---')
        for item in nameUrlList:
            print('Downloading file ',
                  item['name'] + ' from ' + item['url'] + ' ....................................... ')
            download_file(os.path.join('doc', folderName[i], item['name']), item['url'])
        print('--- Done download ---')
    print('==========================================Done download file!=====================================================')


def checkContain(stringNeedCheck, containList):
    for suitName in containList:
        if stringNeedCheck.lower().__contains__(suitName):
            return True
    return False

def write_into_file(nameFile, docs):
    print('docs: ',docs)
    file1 = open(os.path.join(nameFolderDeleteRoot,nameFile), "w",  encoding='UTF-8')
    file1.writelines(docs)
    file1.close()

def delete_file():
    if not os.path.exists(nameFolderDeleteRoot):
        print('*** Create folder '+nameFolderDeleteRoot)
        os.mkdir(nameFolderDeleteRoot)

    for i in range(0,len(folderName)):
        if i==2:
            break
        print('=========================== ' + folderName[i].upper() + ' ======================================')
        if os.path.exists(os.path.join('url', folderName[i] + '.csv')):
            # read urls from file
            print('--- Start read ---')
            print('Read name url of file ', folderName[i] + '.csv')
            nameUrlList = read_file(os.path.join('url', folderName[i] + '.csv'))
            print('Len: ', str(len(nameUrlList)) + ' docs')
            print('--- Done read ---')

            print('--- Start delete wrong format ---')

            fileDeletedList = []
            for item in nameUrlList:
                if not (item['name'].lower().endswith('.doc') or item['name'].lower().endswith('.docx') ) or checkContain(item['name'], containNoSuitNameFileList[i]) or not checkContain(item['name'], containSuitNameFileList[i]) :

                    if os.path.exists(os.path.join('doc', folderName[i], item['name'])):
                        fileDeletedList.append(item['name']+'\n')
                        print('deleting file ', item['name'] + ' ....')
                        os.remove(os.path.join('doc', folderName[i], item['name']))

            # create folder save file contain file deleted
            if not os.path.exists(os.path.join(nameFolderDeleteRoot, folderName[i])):
                # create forder
                print('*** Create folder ' + nameFolderDeleteRoot + '/' + folderName[i])
                os.mkdir(os.path.join(nameFolderDeleteRoot, folderName[i]))
            #save list name of doc was deleted
            write_into_file(os.path.join(folderName[i], folderName[i]+datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.txt")), fileDeletedList)

            print('Total: ',str(len(fileDeletedList)),'files deleted')
            print('--- Done delete ---')
        else:
            print('Don\'t exist file   ' + folderName[i] + '.csv !')


def convert_file_doc_dox_to_txt():
    if not os.path.exists(nameFolderConvertRoot):
        print('*** Create folder ' + nameFolderConvertRoot)
        os.mkdir(nameFolderConvertRoot)
    for i in range(0,len(folderName)):
        print('=========================== ' + folderName[i].upper() + ' ======================================')

        if not os.path.exists(os.path.join(nameFolderConvertRoot, folderName[i])):
            # create forder
            print('*** Create folder '+ nameFolderConvertRoot +'/'+folderName[i])
            os.mkdir(os.path.join(nameFolderConvertRoot, folderName[i]))


        if os.path.exists(os.path.join('url', folderName[i] + '.csv')):
            # read urls from file
            print('--- Start read ---')
            print('Read name url of file ', folderName[i] + '.csv')
            nameUrlList = read_file(os.path.join('url', folderName[i] + '.csv'))
            print('Len: ', str(len(nameUrlList)) + ' docs')
            print('--- Done read ---')

            print('--- Start convert format doc/dox to txt  ---')
            numFileConverted = 0
            for item in nameUrlList:

                newName = item['name'][0:item['name'].rfind(".")] + '.txt'
                if os.path.exists(os.path.join(nameFolderRoot, folderName[i], item['name'])) and not os.path.exists(os.path.join(nameFolderConvertRoot, folderName[i], newName)):
                    try:
                        doc = aw.Document(os.path.join(nameFolderRoot, folderName[i], item['name']))

                        print('converting file '+ item['name'] +' to file '+newName + ' ....')

                        doc.save(os.path.join(nameFolderConvertRoot, folderName[i], newName))

                        numFileConverted = numFileConverted + 1
                    except NameError:
                        print(NameError)
                    except:
                        print("Something else went wrong")
            print('Total: ',str(numFileConverted),'files converted')
            print('--- Done convert ---')
        else:
            print('Don\'t exist file   ' + folderName[i] + '.csv !')

if __name__ == '__main__':
    print('===================== START! ============================')
    # crawl_data()
    delete_file()
    # convert_file_doc_dox_to_txt()
    # temp = '01_2019_ND-CP_404090.doc'
    # containSuitNameFileList = [['nd.cp','nd_cp','nd-cp', 'nđ.cp', 'nđ-cp','nđ_cp']]
    # print(checkContain(temp, containSuitNameFileList[0]))

    # write_into_file('test.txt',['test\n','a\n'])




    print('===================== END! ============================')