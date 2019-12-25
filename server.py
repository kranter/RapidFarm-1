from flask import Flask
from flask import request
from flask import render_template, send_from_directory, abort
import sqlite3

app = Flask(__name__)

db = []
command = None

# api

@app.route('/get_command') 
def give_command():
    global command
    try:
        if command:
            print('command returned: {0}'.format(command))
            return command
    finally:
        command = None
    abort(404)

@app.route('/send_command', methods=['POST']) 
def receive_command():
    global command
    command = request.form['command']
    print(command)
    return 'Ok'

def add_new_data(str_data, AirTemp, WaterTemp, Humidity, LightStatement, AdditInfo):
    with sqlite3.connect('SensorsDB.db') as conn:
        c = conn.cursor()
        tmp = str_data.split(',')
        req = "INSERT INTO \"Sensors Data\"(AirTemp,WaterTemp,Humidity,LightStatement,AdditInfo) VALUES ('%s','%s','%s','%s','%s')"%(AirTemp,WaterTemp,Humidity,LightStatement,AdditInfo);
        c.execute(req)
        conn.commit()

@app.route('/new_data', methods=['POST']) 
def handle_new_data():
    AirTemp = request.args.get('AirTemp')
    WaterTemp = request.args.get('WaterTemp')
    Humidity = request.args.get('Humidity')
    LightStatement = request.args.get('LightStatement')
    AdditInfo = request.args.get('AdditInfo')
    data = request.data
    global db
    clear_data = data
    db.append(clear_data)
    add_new_data(data.decode('ascii'), AirTemp, WaterTemp, Humidity, LightStatement, AdditInfo)

    return 'Success'

# ui

@app.route('/')
def index():
    return render_template('main_page.html', lines=db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
