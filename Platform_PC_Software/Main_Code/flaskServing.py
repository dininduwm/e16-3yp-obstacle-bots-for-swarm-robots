from flask import Flask, render_template, Response, request

# flask initiating
app = Flask(__name__)

# flash camera feed function
def camFeed():
    while True:
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

# falsk thread
def flaskThread(sharedData):
    app.config['frame'] = sharedData
    app.run("0.0.0.0",3001,debug=False)