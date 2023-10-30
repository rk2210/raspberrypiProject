from app import app
from flask import  request, redirect,  url_for, session, jsonify
from .models import Device, Devicetype, Data, db, DataSchema
from .nrf905.nrf905 import Nrf905
import datetime
import sqlite3
import json
 
@app.route('/add_new_data', methods=['POST', 'GET'])
def add_new_data():
    receiver = Nrf905()
    data = receiver.open(433)
    schema = DataSchema()
    result = schema.dump(jsonify(data))
    receiver.close()
    for i in result:
        db.session.add(i)
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

@app.route('/data/<int:device_id>/<string:day>/<string:month>/<string:year>', methods=['GET'])
def get_data_by_posttime(device_id, day, month, year):
    calend = day + '/' + month + '/' + year
    posted_at = datetime.datetime.strptime(calend, '%d/%M/%Y')
    conn = sqlite3.connect('DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM data WHERE device_id = :device_id AND posted_at = :posted_at', {'device_id': device_id, 'posted_at':posted_at})
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

    
