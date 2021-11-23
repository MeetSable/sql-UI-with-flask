from flask import Flask, render_template, request, redirect, url_for
from flask.json import dump

import sql_interface as si
import numpy as np


app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('nav') == 'showTable':
            return redirect(url_for('ShowTable'))
        elif request.form.get('nav') == 'editTable':
            return redirect(url_for('EditTable'))
    return render_template("index.html")
    
@app.route('/table', methods=['GET', 'POST'])
def ShowTable():
    if request.method == 'POST':
        table = request.form.get('tblnam')
        print(table)
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='delivery'")).flatten()
    rows = np.array(si.get_data("select * from delivery"))
    return render_template('table.html', headings=headings, rows = rows)

@app.route('/edit')
def EditTable():
    return 'Editing mode'

    

if __name__ == '__main__':    
    app.run(debug=True)