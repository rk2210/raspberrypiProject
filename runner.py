import os
from app import app, db
from app.models import Device, Devicetype, Data


def make_shell_context():
    return dict(app=app, db=db, Device = Device, Devicetype = Devicetype, Data = Data)



if __name__ == "__main__":
    app.run(debug=True)
