import csv
import math
import os
import re
from collections import Counter
from datetime import datetime

from underthesea import word_tokenize
import xlsxwriter
import numpy as np

nameFolderDataSet = 'dataset'
nameFolderCreateDataSet = 'dataset'
nameFolderConvertRoot = 'convert'
nameFolderVocab = 'vocab'
nameFolderDocList = 'doc-list'
folderName = ['nghiDinh', 'nghiQuyet', 'quyetDinh', 'thongTu']
numberDocEachCategory = 100


def get_stopwords_list(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))

def check_only_same_character(stringNeedCheck):
    if len(stringNeedCheck) <= 1:
        return True
    for i in range(1, len(stringNeedCheck)):
        if stringNeedCheck[i] != stringNeedCheck[0]:
            return False
    return True

def detaching_word_from_file(fileName):
    lines = []
    with open(fileName,encoding='UTF-8') as f:
        contents = f.readlines()
        for line in contents:
            if len(line) >=1 and line!='\n':
                lines.append(word_tokenize(re.sub('\W+',' ', line.lower() ) ))

    lines = lines[2:len(lines)-2]

    # print(lines)

    wordList = []
    for line in lines:
        if len(line)<2:
            continue
        # print(line)
        for item in line:
            if len(item) !=0 and not check_only_same_character(item) and not item.isnumeric() and not item.replace(" ",'').isnumeric() and item not in stopwords:
                wordList.append(item)
    return wordList

def tf(doc):
    term_frequency = Counter(doc)
    tfDict = {}
    for term, count in set(term_frequency.items()):
        if count == 0:
            tfDict[term] = 0
        else:
            tfDict[term] = 1 + math.log10(count)
    return tfDict
    # return doc.count(term)

def idf(docList):
    document_count = len(docList)
    term_document_count = {}
    for document in docList:
        for term in set(document):
            term_document_count[term] = term_document_count.get(term, 0) + 1

    return {term: math.log10(document_count / count) for term, count in term_document_count.items()}
    # numDocContainTerm = 0
    # for doc in docList:
    #     if term in doc:
    #         numDocContainTerm = numDocContainTerm + 1
    # if numDocContainTerm == 0:
    #     return 0
    # return len(docList)/numDocContainTerm

def tfIdf(docList, doc, term):
    return  tf(doc, term) * idf(docList, term)

# tf_scores = [tf(doc) for doc in documents]
# idf_scores = idf(documents)

# Vector representation
def calculate_vector(tf_scores, idf_scores):
    vector = {}
    for  term, tf in tf_scores.items():
        # for term, tf in tf_score.items():
        vector[term] = vector.get(term, 0) + tf * idf_scores[term]
    return vector

# document_vectors = [calculate_vector(tf_score, idf_scores) for tf_score in tf_scores]


def unique_term_list(doc):
    docTemp = list(set(doc))
    docTemp.sort()
    return docTemp

def caculate_tfIdf_docs(docList, doc, docTermUniqueList):
    result = []

    # docTermUnique = unique_term_list(doc)
    for term in docTermUniqueList:
        print('tfIdf term ', term)
        termTfIdf = tfIdf(docList, doc, term)

        result.append({'term': term, 'tfIdf': termTfIdf})
        print('result: ',result )
    return  result

def read_name_doc_from_file(fileNameRead):
    with open(fileNameRead, encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = []
        for row in csv_reader:
            data.append(row[0])
        return list(set(data))

def write_file_excel(fileName, titleList,contentList):
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet("result")

    row = 0
    col = 0
    # worksheet.write(0, 0, 'TERM')
    # worksheet.write(0, 1, 'TFIDF')

    for title in titleList:
        worksheet.write(row, col, title)
        col += 1

    for content in contentList:
        col = 0
        for item in content:
            # worksheet.write(row, col, item['term'])
            worksheet.write(row+1, col, item['tfIdf'])
            col += 1
        row += 1

    workbook.close()



def write_file_excel_with_label(fileName, titleList, contentList,numLabelForEach):
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet("result")

    row = 0
    col = 0

    for title in titleList:
        worksheet.write(row, col, title)
        col += 1

    for content in contentList:
        col = 0
        for item in content:
            # worksheet.write(row, col, item['term'])
            worksheet.write(row + 1, col, item)
            col += 1
        row += 1

    row = 0
    worksheet.write(0, col, 'label')
    for item in folderName:
        for i in range(0,numLabelForEach):
            worksheet.write(row + 1, col, item)
            row += 1

    workbook.close()


def create_dataset():
    if not os.path.exists(nameFolderCreateDataSet):
        print('*** Create folder '+nameFolderCreateDataSet)
        os.mkdir(nameFolderCreateDataSet)

    for i in range(0,len(folderName)):
        print('=========================== ' + folderName[i].upper() + ' ======================================')
        if os.path.exists(os.path.join('url', folderName[i] + '.csv')):
            # read urls from file
            print('--- Start read ---')
            print('Read name url of file ', folderName[i] + '.csv')
            nameList = read_name_doc_from_file(os.path.join('url', folderName[i] + '.csv'))
            print('Len: ', str(len(nameList)) + ' docs')
            print('--- Done read ---')

            print('--- Start create dataset ---')

            wordList = []
            for item in nameList:
                if '.docx' in item:
                    newName = item.replace('.docx','.txt')
                elif '.DOCX' in item:
                    newName = item.replace('.DOCX','.txt')
                elif '.DOC' in item:
                    newName = item.replace('.DOC','.txt')
                else:
                    newName = item.replace('.doc', '.txt')
                if os.path.exists(os.path.join(nameFolderConvertRoot, folderName[i], newName)):
                    # fileDeletedList.append(item['name']+'\n')
                    print('read and detaching word from file ', newName + ' ....')
                    # os.remove(os.path.join('doc', folderName[i], item['name']))
                    wordList1 = detaching_word_from_file(os.path.join(nameFolderConvertRoot, folderName[i], newName))
                    wordList.append(wordList1)


            wordUniqueList = []
            for doc in wordList:
                if len(wordUniqueList) == 0:
                    wordUniqueList = list(set(doc))
                else:
                    wordUniqueList = list(set(wordUniqueList).union(set(doc)))
            wordUniqueList.sort()

            result = []
            for doc in wordList:
                result.append(caculate_tfIdf_docs(wordList, doc, wordUniqueList))

            # create folder save file dataset follow each category
            if not os.path.exists(os.path.join(nameFolderCreateDataSet, folderName[i])):
                # create forder
                print('*** Create folder ' + nameFolderCreateDataSet + '/' + folderName[i])
                os.mkdir(os.path.join(nameFolderCreateDataSet, folderName[i]))

            #save tfidf of doc
            if len(result)!=0:
                write_file_excel(
                    os.path.join(nameFolderCreateDataSet,folderName[i], folderName[i] + datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.xlsx")),
                    wordUniqueList, result)

            print('Total: ',str(len(wordUniqueList)),' tokens')
            print('--- Done create dataset ---')


        else:
            print('Don\'t exist file   ' + folderName[i] + '.csv !')

def create_dataset_one_file():
    global nameFileVocab
    global nameFileDocList
    vocabs = np.load(nameFileVocab, allow_pickle=True)
    docList = np.load(nameFileDocList, allow_pickle=True)

    tf_scores = [tf(doc) for doc in docList]
    # print(tf_scores)
    idf_scores = idf(docList)
    # print(idf_scores)
    document_vectors = [calculate_vector(tf_score, idf_scores) for tf_score in tf_scores]
    # print(document_vectors)

    matrix = list(np.zeros((docList.shape[0], vocabs.shape[0]), dtype=float))

    indexDoc = 0
    for vector in document_vectors:
        for term, idfScore in vector.items():
            termIndex = np.where(vocabs == term)[0]
            matrix[indexDoc][termIndex] = idfScore
        indexDoc += 1


    if not os.path.exists(nameFolderCreateDataSet):
        print('*** Create folder '+nameFolderCreateDataSet)
        os.mkdir(nameFolderCreateDataSet)

    # create folder save file dataset follow each category
    if not os.path.exists(os.path.join(nameFolderCreateDataSet, 'all')):
        # create forder
        print('*** Create folder ' + nameFolderCreateDataSet + '/' + 'all')
        os.mkdir(os.path.join(nameFolderCreateDataSet, 'all'))



    #save tfidf of doc
    write_file_excel_with_label(
        os.path.join(nameFolderCreateDataSet,'all','dataset' + datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.xlsx")),
        vocabs, matrix,numberDocEachCategory)

    print('Total: ',str(len(vocabs)),' tokens')
    print('       ', str(len(docList)), ' docs')
    print('--- Done create dataset ---')

def save_vocab_and_doc_list():
    if not os.path.exists(nameFolderVocab):
        print('*** Create folder '+nameFolderVocab)
        os.mkdir(nameFolderVocab)

    if not os.path.exists(nameFolderDocList):
        print('*** Create folder '+nameFolderDocList)
        os.mkdir(nameFolderDocList)

    wordList = []


    for i in range(0,len(folderName)):
        print('=========================== ' + folderName[i].upper() + ' ======================================')
        if os.path.exists(os.path.join('url', folderName[i] + '.csv')):
            # read urls from file
            print('--- Start read ---')
            print('Read name url of file ', folderName[i] + '.csv')
            nameList = read_name_doc_from_file(os.path.join('url', folderName[i] + '.csv'))
            print('Len: ', str(len(nameList)) + ' docs')
            print('--- Done read ---')

            countReadedDoc = 0
            for item in nameList:
                if '.docx' in item:
                    newName = item.replace('.docx','.txt')
                elif '.DOCX' in item:
                    newName = item.replace('.DOCX','.txt')
                elif '.DOC' in item:
                    newName = item.replace('.DOC','.txt')
                else:
                    newName = item.replace('.doc', '.txt')
                if os.path.exists(os.path.join(nameFolderConvertRoot, folderName[i], newName)):
                    print('read and detaching word from file ', newName + ' ....')
                    wordList1 = detaching_word_from_file(os.path.join(nameFolderConvertRoot, folderName[i], newName))
                    wordList.append(wordList1)
                    countReadedDoc +=1
                    if countReadedDoc == numberDocEachCategory:
                        break

    print('--- Start save vocabs and doc list ---')
    wordUniqueList = []
    for doc in wordList:
        if len(wordUniqueList) == 0:
            wordUniqueList = list(set(doc))
        else:
            wordUniqueList = list(set(wordUniqueList).union(set(doc)))
    wordUniqueList.sort()

    global nameFileVocab
    global  nameFileDocList
    nameFileVocab =os.path.join(nameFolderVocab, nameFolderVocab + datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.npy"))
    nameFileDocList = os.path.join(nameFolderDocList, nameFolderDocList + datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.npy"))
    print('Save file '+nameFileVocab)
    np.save( nameFileVocab,wordUniqueList , allow_pickle=True)
    print('Save file '+nameFileDocList)
    np.save( nameFileDocList,wordList , allow_pickle=True)

    print('Total: ',str(len(wordUniqueList)),' tokens')
    print('--- Done create dataset ---')


if __name__ == '__main__':

    print('---------------------START----------------------')
    stopwords = get_stopwords_list('vietnamese-stopwords.txt')
    # print(stopwords)
    #
    # fileName = '01.2015.ND.CP.txt'
    # wordList1 = detaching_word_from_file(fileName)
    # print(wordList1)
    #
    # fileName2 = '01.2016.ND.CP.txt'
    # wordList2 = detaching_word_from_file(fileName2)
    # print(wordList2)
    #
    # wordList = list(set(wordList1).union(set(wordList2)))
    # wordList.sort()
    # print(wordList)
    #
    # docList = [wordList1,wordList2]
    #
    #
    # doc = ['a', 'a', 'a', 'a', 'b','b', 'c', 'c']
    # docList=[['a', 'a', 'a', 'a', 'b', 'c', 'c'], ['a', 'a', 'a', 'a', 'c', 'c'],['a', 'a', 'a', 'a', 'a', 'b', 'c', 'c']]
    # # print(tfIdf(docList, doc, 'b'))
    # result = []
    # for doc in docList:
    #     result.append(caculate_tfIdf_docs(docList, doc, wordList))
    #
    # print(result)
    #
    # # write_file_txt('myfile.txt')
    # write_file_excel('nghiDinh.xlsx',wordList, result)

    # create_dataset()

    save_vocab_and_doc_list()

    create_dataset_one_file()



    # tf_scores = [tf(doc) for doc in docList]
    # print(tf_scores)
    # idf_scores = idf(docList)
    # print(idf_scores)
    # document_vectors = [calculate_vector(tf_score, idf_scores) for tf_score in tf_scores]
    # print(document_vectors)

    print('---------------------END----------------------')
