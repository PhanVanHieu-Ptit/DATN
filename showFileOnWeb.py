import subprocess
import os

def convert_doc_to_pdf(doc_file):
    # Chuyển đổi tệp DOC thành PDF bằng unoconv
    pdf_file = doc_file.replace('.doc', '.pdf')
    subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_file, doc_file])

    return pdf_file

def display_pdf_on_web(pdf_file):
    # Hiển thị tệp PDF trên web
    # Đây chỉ là một ví dụ cơ bản, bạn có thể sử dụng các thư viện web framework như Flask hoặc Django để hiển thị tệp PDF trên web.
    # Đoạn mã này sử dụng Flask để hiển thị tệp PDF.
    from flask import Flask, send_file

    app = Flask(__name)

    @app.route('/pdf')
    def serve_pdf():
        return send_file(pdf_file, as_attachment=False)

    app.run()

if __name__ == '__main__':
    doc_file = 'path_to_your_doc_file.doc'
    pdf_file = convert_doc_to_pdf(doc_file)
    display_pdf_on_web(pdf_file)
