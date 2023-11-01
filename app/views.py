from app import app
from flask import  request, redirect,  url_for, session, jsonify
from .models import Device, Devicetype, Data, db, DataSchema
from .nrf905.nrf905 import Nrf905
from datetime import date
import sqlite3
import json
 
@app.route('/add_new_data', methods=['POST', 'GET'])
def add_new_data():
    receiver = Nrf905()
    data = receiver.open(433)
    schema = DataSchema()
    result = schema.dump(jsonify(data))
    receiver.close()
    db.session.add(result)
    db.session.commit()
    return 'Data is succesfully commited!'

@app.route('/devicelist', methods=['GET'])
def get_devicelist():
    conn = sqlite3.connect('DataDevices.db')
    curs = conn.cursor()
    curs.execute('select * from devices')
    result = curs.fetchall()
    curs.close()
    conn.close()
    return jsonify(result)

@app.route('/get_data_by_postdate', methods=['GET'])
def get_data_by_posttime():
    year_start = int(input('Enter start year: '))
    month_start = int(input('Enter start month: '))
    date_start = int(input('Enter start date: '))
    posted_at_start = date(year_start, month_start, date_start)
    year_finish = int(input('Enter finish year: '))
    month_finish = int(input('Enter finish month: '))
    date_finish = int(input('Enter finish date: '))
    posted_at_finish = date(year_finish, month_finish, date_finish)
    conn = sqlite3.connect('DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM data WHERE :posted_at_finish > posted_at > :posted_at_start', {'posted_at_finish':posted_at_finish, 'posted_at_start':posted_at_start})
    result = curs.fetchall()
    curs.close()
    conn.close()
    return jsonify(result)
    
@app.route('/device/<int:device_id>', methods=['GET'])
def get_device_by_id(device_id):
    conn = sqlite3.connect('DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM devices WHERE _id = :device_id', {'device_id': device_id})
    result = curs.fetchall()
    curs.close()
    conn.close()
    return jsonify(result)

    
