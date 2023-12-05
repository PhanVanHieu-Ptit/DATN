import os
import aspose.words as aw
import numpy as np
from datetime import datetime
from preHandle import detaching_word_from_file_with_stopwords, tf, idf, calculate_vector, write_file_excel_with_label, \
    write_csv_file

nameFolderCreateDataSet = 'dataset'
numberDocEachCategory=100
nameFolderDocPredict = 'doc-predict'
nameFolderCreateDatasSetWithNewDoc = 'all-with-new_doc'
nameFolderCreateDatasSetWithDocUpload = 'uploads'
nameFolderDocPredictConvert = 'convert-doc-predict'
fileNameNeedPredict = 'TT.52.2022.TT.BGTVT.doc.docx'
nameFileVocab = './vocab/vocab_2023-10-28_23--18--36.npy'
nameFileDocList = './doc-list/doc-list_2023-10-28_20--51--57.npy'

def get_stopwords_list(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))

def convert_one_doc_to_txt(fileName):
    if not os.path.exists(nameFolderDocPredictConvert):
        print('*** Create folder ' + nameFolderDocPredictConvert)
        os.mkdir(nameFolderDocPredictConvert)

    if os.path.exists(os.path.join(nameFolderDocPredict, fileName)):
        print('======= Start convert ======')
        newName = fileName[:fileName.rfind(".")] + '.txt'
        try:
            doc = aw.Document(os.path.join(nameFolderDocPredict, fileName))

            print('converting file ' + fileName + ' to file ' + newName + ' ....')

            doc.save(os.path.join(nameFolderDocPredictConvert, newName))
        except NameError:
            print(NameError)
        except:
            print("Something else went wrong")
    print('======= Done convert! ======')

def convert_one_doc_upload_to_txt(fileName):
    if not os.path.exists(nameFolderDocPredictConvert):
        print('*** Create folder ' + nameFolderDocPredictConvert)
        os.mkdir(nameFolderDocPredictConvert)

    if not os.path.exists(os.path.join(nameFolderDocPredictConvert,nameFolderCreateDatasSetWithDocUpload)):
        print('*** Create folder ' + nameFolderDocPredictConvert+'/'+nameFolderCreateDatasSetWithDocUpload)
        os.mkdir(os.path.join(nameFolderDocPredictConvert,nameFolderCreateDatasSetWithDocUpload))

    if os.path.exists(os.path.join(nameFolderCreateDatasSetWithDocUpload, fileName)):
        print('======= Start convert ======')
        newName = fileName[:fileName.rfind(".")] + '.txt'
        try:
            doc = aw.Document(os.path.join(nameFolderCreateDatasSetWithDocUpload, fileName))

            print('converting file ' + fileName + ' to file ' + newName + ' ....')

            doc.save(os.path.join(nameFolderDocPredictConvert,nameFolderCreateDatasSetWithDocUpload, newName))
        except NameError:
            print(NameError)
        except:
            print("Something else went wrong")
    print('======= Done convert! ======')

def calculator_tfidf(fileName,):
    vocabs = np.load(nameFileVocab, allow_pickle=True)
    docList = np.load(nameFileDocList, allow_pickle=True)
    wordList = detaching_word_from_file_with_stopwords(os.path.join(nameFolderDocPredictConvert, fileName[:fileName.rfind(".")] + '.txt'),stopwords)
    wordListSuitWithVocabs = [word for word in wordList if word in vocabs]

    docList = docList.tolist()
    docList.append(wordListSuitWithVocabs)

    docList = np.array(docList, dtype=object)

    tf_scores = [tf(doc) for doc in docList]
    idf_scores = idf(docList)
    # document_vectors = [calculate_vector(tf_score, idf_scores) for tf_score in tf_scores]

    document_vectors = [calculate_vector(tf_scores[-1],idf_scores)]
    # matrix = list(np.zeros((docList.shape[0], vocabs.shape[0]), dtype=float))
    matrix = list(np.zeros((1, vocabs.shape[0]), dtype=float))

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
    if not os.path.exists(os.path.join(nameFolderCreateDataSet,nameFolderCreateDatasSetWithNewDoc)):
        # create forder
        print('*** Create folder ' + nameFolderCreateDataSet + '/' + nameFolderCreateDatasSetWithNewDoc)
        os.mkdir(os.path.join(nameFolderCreateDataSet, nameFolderCreateDatasSetWithNewDoc))

    #save tfidf of doc
    nameTfIdfDocPredict = os.path.join(nameFolderCreateDataSet,nameFolderCreateDatasSetWithNewDoc,'dataset' + datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.xlsx"))
    write_file_excel_with_label(
        nameTfIdfDocPredict,
        vocabs, matrix,numberDocEachCategory)

    print('Total: ',str(len(wordListSuitWithVocabs)), 'tokens suit of new doc')
    print('       '+str(len(vocabs)),' tokens of dataset')
    print('       ', str(len(docList)), ' docs dataset')
    print('--- Done create dataset ---')
    return nameTfIdfDocPredict

def calculator_tfidf_with_stop_word(fileName,stopwords):
    print('--- Start calculator tfidf ---')
    vocabs = np.load(nameFileVocab, allow_pickle=True)
    docList = np.load(nameFileDocList, allow_pickle=True)
    wordList = detaching_word_from_file_with_stopwords(os.path.join(nameFolderDocPredictConvert,nameFolderCreateDatasSetWithDocUpload, fileName[:fileName.rfind(".")] + '.txt'),stopwords)
    wordListSuitWithVocabs = [word for word in wordList if word in vocabs]

    print('vocabs.shape[0]: ',vocabs.shape[0])

    docList = docList.tolist()
    docList.append(wordListSuitWithVocabs)

    docList = np.array(docList, dtype=object)

    tf_scores = [tf(doc) for doc in docList]
    idf_scores = idf(docList)
    # document_vectors = [calculate_vector(tf_score, idf_scores) for tf_score in tf_scores]

    document_vectors = [calculate_vector(tf_scores[-1],idf_scores)]
    # matrix = list(np.zeros((docList.shape[0], vocabs.shape[0]), dtype=float))
    matrix = list(np.zeros((1, vocabs.shape[0]), dtype=float))

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
    if not os.path.exists(os.path.join(nameFolderCreateDataSet,nameFolderCreateDatasSetWithDocUpload)):
        # create forder
        print('*** Create folder ' + nameFolderCreateDataSet + '/' + nameFolderCreateDatasSetWithDocUpload)
        os.mkdir(os.path.join(nameFolderCreateDataSet, nameFolderCreateDatasSetWithDocUpload))

    #save tfidf of doc
    nameTfIdfDocPredict = os.path.join(nameFolderCreateDataSet,nameFolderCreateDatasSetWithDocUpload,'dataset' + datetime.now().strftime("_%Y-%m-%d_%H--%M--%S.csv"))
    # write_file_excel_with_label(
    #     nameTfIdfDocPredict,
    #     vocabs, matrix,0,True)
    write_csv_file(nameTfIdfDocPredict, vocabs.tolist(),
                   np.array(matrix).tolist())

    print('Total: ',str(len(vocabs)),' tokens')
    print('       ', str(len(docList)), ' docs')
    print('--- Done create dataset ---')
    return nameTfIdfDocPredict



if __name__ == '__main__':
    print('=====================================START PROGRAMMING=========================================')
    global stopwords
    stopwords = get_stopwords_list('vietnamese-stopwords.txt')
    convert_one_doc_to_txt(fileNameNeedPredict)
    calculator_tfidf(fileNameNeedPredict)
    print('=====================================END PROGRAMMING=========================================')
