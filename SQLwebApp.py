from flask import Flask, render_template, request, redirect, url_for

from flask.json import dump

import sql_interface as si
import numpy as np


app = Flask(__name__, template_folder='templates')

#home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('nav') == 'showTable':
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('nav') == 'editTable':
            return redirect(url_for('selectTabletoShow'))
    return render_template("index.html")

@app.route('/table', methods=['GET','POST'])
def selectTabletoShow():
    if request.method == 'POST':
        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('ShowTable', tableName=tableName))
    return render_template('selectTable.html')
        
@app.route('/EditTable', methods=['GET','POST'])
def selectTabletoEdit():
    if request.method == 'POST':
        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('EditTable', tableName=tableName))
    return render_template('editTable.html')

# display tables   
@app.route('/table/<tableName>', methods=['GET', 'POST'])
def ShowTable(tableName):    
    if request.method == 'POST':
        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('ShowTable', tableName=tableName))
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='{}'".format(tableName))).flatten()
    rows = np.array(si.get_data("select * from {}".format(tableName)))
    return render_template('table.html', headings=headings, rows = rows)


# Insert in table
@app.route('/edit/<tableName>', methods=['GET', 'POST'])
def EditTable(tableName):
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='{}'".format(tableName))).flatten()
    return render_template('editTable.html', headings=headings)

    

if __name__ == '__main__':    
    app.run(debug=True)