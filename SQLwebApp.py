from flask import Flask, render_template, request, redirect, url_for

from flask.json import dump
from numpy.lib import type_check
import webbrowser
import sql_interface as si
import numpy as np


app = Flask(__name__, template_folder='templates', static_folder='static')

tables = [  "all_manufacturing_machines", "contacts", "contacts_details", "delivery", "departments", "driver_details", "employee", "employee_type", "manufacturing_machines", "material_providers",
            "raw_material_orders", "raw_materials", "sales", "shop_details", "shop_orders", "toy_base", "toy_materials", "toy_types"]

#home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))
        elif request.form.get('customQuery'):
            return redirect(url_for('customQuery'))
    return redirect(url_for('selectTabletoShow'))

#Custom query
@app.route('/custom', methods=['GET', 'POST'])
def customQuery():
    query = request.args.get('query')
    if query == None:
        query = ''   

    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))

        elif request.form.get('Submit'):
            query = request.form.get('query')
            print(query)
            return redirect(url_for('customTable', query=query))

    return render_template('customQuery.html', query=query)

#custom Table show
@app.route('/custom/query', methods=['GET', 'POST'])
def customTable():
    query = request.args.get('query')
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))

        elif request.form.get('Submit'):
            query = request.form.get('query')
            return redirect(url_for('customTable', query=query))
    data = si.get_data(query)
    if data == None:
        return redirect(url_for('customQuery', query=query))
    return render_template('customTable.html', data=data, query=query)

#Table selceiotn page to show
@app.route('/table', methods=['GET','POST'])
def selectTabletoShow():
    if request.method == 'POST':
        if request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))
        elif request.form.get('customQuery'):
            return redirect(url_for('customQuery'))

        if request.form.get('tblnam')!= 'nothing':
            tableName = request.form.get('tblnam')
            print(tableName)
            return redirect(url_for('ShowTable', tableName=tableName))
    return render_template('selectTable.html', tables=tables)

#Table Select for editing    
@app.route('/edit', methods=['GET','POST'])
def selectTabletoEdit():
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('customQuery'):
            return redirect(url_for('customQuery'))

        if request.form.get('tblnam')!= 'nothing':
            tableName = request.form.get('tblnam')
            print(tableName)
            return redirect(url_for('EditTable', tableName=tableName))
    return render_template('editTable.html', tables=tables)

# display tables   
@app.route('/table/<tableName>', methods=['GET', 'POST'])
def ShowTable(tableName):
    if tableName not in tables:
        return redirect(url_for('selectTabletoShow'))    
    if request.method == 'POST':
        if request.form.get('editTable'):
            return redirect(url_for('selectTabletoEdit'))
        elif request.form.get('customQuery'):
            return redirect(url_for('customQuery'))

        tableName = request.form.get('tblnam')
        print(tableName)
        return redirect(url_for('ShowTable', tableName=tableName))
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='{}'  ORDER BY ORDINAL_POSITION ".format(tableName))).flatten()
    rows = np.array(si.get_data("select * from {}".format(tableName)))
    return render_template('table.html', headings=headings, rows = rows, tableName=tableName, tables=tables)


# Insert in table
@app.route('/edit/<tableName>', methods=['GET', 'POST'])
def EditTable(tableName):
    headings = np.array(si.get_data("select column_name from information_schema.columns where table_name='{}'  ORDER BY ORDINAL_POSITION ".format(tableName))).flatten()
    if tableName not in tables:
        return redirect(url_for('selectTabletoEdit'))
    if request.method == 'POST':
        if request.form.get('showTable'):
            return redirect(url_for('selectTabletoShow'))
        elif request.form.get('customQuery'):
            return redirect(url_for('customQuery'))

        elif request.form.get('Submit'):
            query = 'insert into {}('.format(tableName) + ', '.join(['%s' for _ in range(len(headings))]) + ') values(' + ', '.join(['\'%s\'' for _ in range(len(headings))]) + ')'
            temp = headings
            for i in headings:
                temp = np.append(temp, request.form.get(i))
            temp = tuple(temp)
            query = query% temp
            print(query)
            # si.insert_data(query)
        elif request.form.get('tblnam') != 'nothing':
            tableName = request.form.get('tblnam')
            print(tableName)
            return redirect(url_for('EditTable', tableName=tableName))
    return render_template('edit.html', headings=headings, tableName=tableName, tables=tables)

    
if __name__ == '__main__':    
    app.run(debug=True, port=5000)