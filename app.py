from flask import Flask, render_template, request
import misc
import os

app = Flask(__name__)

app.config['UPLOADED_CSV_DEST'] = 'uploads/'


@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    if request.method == 'POST' and 'csv' in request.files:
        csv_file = request.files['csv']
        if csv_file:
            filepath = os.path.join(app.config['UPLOADED_CSV_DEST'], csv_file.filename)
            csv_file.save(filepath)
            misc.create_user_table()
            misc.populate_user_table(misc.read_csv_iterator(filepath))

    filters = {param: value for param, value in request.args.items() if value} if request.method == 'GET' else None
    data = misc.get_filtered_data(per_page, page, filters)
    return render_template('index.html', data=data, page=page, per_page=per_page)

if __name__ == '__main__':
    app.run(debug=True)
