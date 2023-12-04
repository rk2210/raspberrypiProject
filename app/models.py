from app import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from marshmallow import Schema, fields, post_load

class  Devicetype(db.Model):
    __tablename__ = 'types_of_devices'
    _id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    device = db.relationship('Device', backref='devicetype')


class Device(db.Model):
    __tablename__ = 'devices'
    _id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.Integer(), nullable = False)
    description = db.Column(db.String(256), nullable=False)
    device_type = db.Column(db.String(256), db.ForeignKey('types_of_devices._id'))
    data = db.relationship('Data', backref='device')
   

class Data(db.Model):
    __tablename__ = 'data'
    _id = db.Column(db.Integer(), primary_key=True)
    statusmod = db.Column(db.String(256), db.ForeignKey('statusmodels.name'))
    data = db.Column(db.JSON(), nullable=False)
    posted_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable = False)
    device_id = db.Column(db.Integer(), db.ForeignKey('devices._id'))


        
class Statusmodel(db.Model):
    __tablename__ = 'statusmodels'
    name = db.Column(db.String(256), primary_key=True)
    data = db.relationship('Data', backref='status')


class DataSchema(Schema):
    _id = fields.Integer(dump_only=True)
    statusmod = fields.String()
    data = fields.Raw()
    posted_at = fields.DateTime(dump_only=True)
    device_id = fields.Integer()

    @post_load
    def make_data(self, data, **kwargs):
        return Data(**data)

class DateForm(FlaskForm):
    startdate = DateField("Enter start date", format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField("Enter end date", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Check")