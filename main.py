
from flask import Flask, render_template, Response, request, jsonify

from Database import *
import json
from google.api_core.datetime_helpers import DatetimeWithNanoseconds



app = Flask(__name__)
@app.route('/')
def index():

    docs = get_sensor_readings()

    myObjects = []
    for doc in docs:
        myObjects.append(doc.to_dict())
    print(myObjects)
    return render_template('index.html', sensor_readings = myObjects)

@app.route('/api/sensor_readings')
def sensor_readings():

    docs = get_sensor_readings()

    myObjects = []
    for doc in docs:
        myObjects.append(doc.to_dict())
    print(myObjects)

    new_object = []
    for item in myObjects:
        print(item)
        Started_At = str(item['Started_At'].year) + '.' + str(item['Started_At'].month) + '.' + str(item['Started_At'].day) + ':' + str(item['Started_At'].hour) + '.' + str(item['Started_At'].minute) + '.' + str(item['Started_At'].second) 
        new_item = {"NAME":item['NAME'], "Started_At":Started_At, "Liters":item['Liters'], "Duration":item['Duration']}
        new_object.append(new_item)

    return json.dumps(new_object)


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080)
