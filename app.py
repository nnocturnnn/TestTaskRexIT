from flask import Flask, render_template, request
import sqlite3
import misc
import os

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    if request.method == 'POST' and 'csv' in request.files:
        csv_file = request.files['csv']
        if csv_file:
            csv_file.save(os.path.join(app.config['UPLOADED_CSV_DEST'], csv_file.filename))
    return render_template('index.html', data=misc.get_data(per_page, page), page=page, per_page=per_page)

if __name__ == '__main__':
    app.run(debug=True)
