from flask import Flask, render_template, Response, request
import time
import json

# flask initiating
app = Flask(__name__)

# flash camera feed function
def camFeed():
    while True:
        time.sleep(0.1)
        img = app.config['frame'][1]
        # print ('image =======', img)

        yield (b'--frame\r\n' 
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  

#--------------Static serving--------------#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/style.css')
def style():
	return render_template('style.css')

@app.route('/app.js')
def js():
	return render_template('app.js')

@app.route('/video_feed')
def video_feed():
    return Response(camFeed(), mimetype='multipart/x-mixed-replace; boundary=frame')


# routs for the programme functions
@app.route('/start')
def start():
    print('Process started')
    app.config['frame'][2] = True
    return "hello world"

@app.route('/pause')
def pause():
    print('Process paused')
    app.config['frame'][2] = False
    return "hello world"

@app.route('/home')
def home():
    print('Home')
    data = [
        {
            'x': 417,
            'y': 445,
        },
        {
            'x': 515,
            'y': 445,
        },
    ]
    app.config['frame'][3] = json.dumps(data)
    return "hello world"

@app.route('/home_1')
def homeBot_1():
    print('Home')
    data = [
        {
            'x': 515,
            'y': 445,
        },
    ]
    app.config['frame'][3] = json.dumps(data)
    return "hello world"

@app.route('/home_2')
def homeBot_2():
    print('Home')
    data = [
        {
            'x': 417,
            'y': 445,
        },
    ]
    app.config['frame'][3] = json.dumps(data)
    return "hello world"

# falsk thread
def flaskThread(sharedData):
    app.config['frame'] = sharedData
    app.run("0.0.0.0",3001,debug=False)