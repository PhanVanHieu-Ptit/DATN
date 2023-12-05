import os
from flask import Flask, render_template, request, redirect, send_from_directory, send_file
import joblib
import pandas as pd
import numpy as np
import aspose.words as aw

from predictDoc import get_stopwords_list, calculator_tfidf_with_stop_word, \
    convert_one_doc_upload_to_txt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MODEL_FOLDER'] = 'models'

stopwords = get_stopwords_list('vietnamese-stopwords.txt')

col_names = np.load('./vocab/vocab_2023-10-28_23--18--36.npy', allow_pickle=True)


print('len(col_names): ',len(col_names))

def label(x):
    switcher = {
        'nghiDinh': 'Nghị định',
        'nghiQuyet': 'Nghị quyết',
        'quyetDinh': 'Quyết định',
        'thongTu': 'Thông tư',
    }
    return switcher.get(x, "Không xác định")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        filePdf = filename.replace('.doc','.pdf')
        doc = aw.Document(filename)
        doc.save(filePdf)

        # return render_template('index.html',
        #                        pdf_file_path=filePdf)

        convert_one_doc_upload_to_txt(file.filename)
        nameTfIdfDocPredict = calculator_tfidf_with_stop_word(file.filename,stopwords)

        print('nameTfIdfDocPredict: ',nameTfIdfDocPredict)

        # pima = pd.read_excel(nameTfIdfDocPredict)
        pima = pd.read_csv(nameTfIdfDocPredict, encoding='UTF-8')
        X = pima[col_names]

        model_name = request.form.get('model_name')

        model_path = os.path.join(app.config['MODEL_FOLDER'], f'{model_name}')
        print('model_name: ',model_name)
        print('model_path: ', model_path)
        model = joblib.load(model_path)

        result = model.predict([X.loc[len(X)-1]])
        print('result: ',result)

        if model_name =='decision_tree_model_2023-11-12_03--37--28-95.joblib':
            model_name = 'Cây quyết định'
        else:
            model_name = 'SVM'

        return render_template('index.html', result=label(result[0]),history=f"Tệp: {file.filename} Mô hình: {model_name}, Kết quả dự đoán: {label(result[0])}", pdf_file_path=filePdf)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)


