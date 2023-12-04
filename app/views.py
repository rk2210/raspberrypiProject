from app import app
from flask import request, redirect,  url_for, session, jsonify, render_template
from .models import db, DataSchema, DateForm
#from .nrf905.nrf905 import Nrf905
from datetime import date
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

@app.route('/get_data_by_postdate', methods=['GET'])
def get_data_by_posttime():
    form = DateForm()
    render_template('data_by_postdate.html', form=form)
    posted_at_start = request.form.get('startdate')
    posted_at_finish = request.form.get('enddate')
    conn = sqlite3.connect('instance/DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM data WHERE :posted_at_finish > posted_at > :posted_at_start', {'posted_at_finish': posted_at_finish, 'posted_at_start': posted_at_start})
    result = curs.fetchall()
    curs.close()
    conn.close()
    return render_template('data_by_postdate.html', form=form)
    
@app.route('/device/<int:device_id>', methods=['GET'])
def get_device_by_id(device_id):
    conn = sqlite3.connect('instance/DataDevices.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM devices WHERE _id = :device_id', {'device_id': device_id})
    result = curs.fetchall()
    curs.close()
    conn.close()
    return jsonify(result)


    
