from app import app
from flask import request, redirect,  url_for, session, jsonify, render_template
from .models import db, DataSchema, DateForm
#from .nrf905.nrf905 import Nrf905
import datetime
import sqlite3
import json


 
@app.route('/add_new_data', methods=['POST', 'GET'])
def add_new_data():
    #receiver = Nrf905()
    #data = receiver.open(433)
    datadev = {
        'statusmod':'ON',
        'data': {
            'amperage': 50,
            'address': 138675,
            'user': 'Ivan23'
        },
        'device_id':1
    }
    schema = DataSchema()
    result = schema.load(datadev)
    #receiver.close()
    db.session.add(result)
    db.session.commit()
    return 'Data is succesfully commited!'

@app.route('/devicelist', methods=['GET'])
def get_devicelist():
    conn = sqlite3.connect('instance/DataDevices.db')
    curs = conn.cursor()
    curs.execute('select * from devices')
    result = curs.fetchall()
    curs.close()
    conn.close()
    return jsonify(result)

@app.route('/get_data_by_postdate')
def get_data_by_postdate():
    conn = sqlite3.connect('instance/DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM data')
                 #WHERE :posted_at_finish > posted_at > :posted_at_start', {'posted_at_finish': posted_at_finish, 'posted_at_start': posted_at_start})
    result = curs.fetchall()
    curs.close()
    conn.close()
    return result


@app.route('/verify', methods=['POST'])
def verify():
    posted_at_start = request.form['startdate']
    posted_at_finish = request.form['enddate']
    return redirect(f'/get_data_by_postdate/result/{posted_at_start}/{posted_at_finish}')

@app.route('/get_data_by_postdate/result/<posted_at_start>/<posted_at_finish>', methods=['GET', 'POST'])
def result(posted_at_start, posted_at_finish):
    conn = sqlite3.connect('instance/DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM data')
                 #WHERE :posted_at_finish > posted_at > :posted_at_start', {'posted_at_finish': posted_at_finish, 'posted_at_start': posted_at_start})
    result = curs.fetchall()
    curs.close()
    conn.close()
    print(result)
    return f'Result:{result}'

    
@app.route('/device/<int:device_id>', methods=['GET'])
def get_device_by_id(device_id):
    conn = sqlite3.connect('instance/DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM devices WHERE _id = :device_id', {'device_id': device_id})
    result = curs.fetchall()
    curs.close()
    conn.close()
    return jsonify(result)


    
