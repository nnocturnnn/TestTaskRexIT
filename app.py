from flask import Flask, render_template, request
import misc
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    filters = None

    if request.method == 'POST' and 'csv' in request.files:
        csv_file = request.files['csv']
        if csv_file:
            csv_file.save(os.path.join(app.config['UPLOADED_CSV_DEST'], csv_file.filename))

    if request.method == 'GET':
        filter_params = ['category', 'gender', 'dob', 'min_age', 'max_age']
        filters = {param: value for param, value in request.args.items() if value}
    print(filters)
    data = misc.get_filtered_data(per_page, page, filters)
    return render_template('index.html', data=data, page=page, per_page=per_page)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
