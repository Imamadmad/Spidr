from flask import *
import requests
import base64
import api_auth
import json

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('upload.html')

@app.route('/identify', methods=['POST'])
def spider():

    if 'upload' not in request.files:
        return redirect(request.url)

    img = request.files['upload'].read()

    json_header = {'Content-Type': 'application/json'}

    auth = (api_auth.USER, api_auth.PASS)
    b64img = base64.b64encode(img).decode()

    data = '{"service":"%s","image":"%s"}'%('spider',b64img)

    uploaded_task = requests.post(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
        data = data,
        auth = auth,
        headers = json_header
    )

    resp = uploaded_task.json()
    print(resp)

    id = resp['task']['uri'].split('/')[-1]

    scan_task = requests.put(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/run/{}'.format(id),
        data = '{"scanned": true}',
        auth = auth,
        headers = json_header
    )

    resp = scan_task.json()['task']
    print(resp)

    desc = resp['description']
    confidence = resp['confidence']

    return 'description: {}, confidence: {}'.format(desc, confidence)

@app.route('/identifyMob', methods=['POST'])
def spiderMob():

    if 'upload' in request.files:
        b64img = base64.b64encode(request.files['upload'].read()).decode()
    elif 'imageData' in request.form:
        b64img = request.form['imageData']

    json_header = {'Content-Type': 'application/json'}

    auth = (api_auth.USER, api_auth.PASS)

    data = '{"service":"%s","image":"%s"}'%('spiders',b64img)

    uploaded_task = requests.post(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
        data = data,
        auth = auth,
        headers = json_header
    )

    resp = uploaded_task.json()
    print(resp)

    id = resp['task']['uri'].split('/')[-1]

    scan_task = requests.put(
        'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/run/{}'.format(id),
        data = '{"scanned": true}',
        auth = auth,
        headers = json_header
    )

    print(scan_task.text)
    resp = scan_task.json()['task']

    desc = resp['description']
    confidence = float(resp['confidence'])

    if confidence < 60:
        return json.dumps({
            "name": "try_again"
        })

    return json.dumps({
        "name": desc
    })

@app.route('/result')
def dummy() :
    info = {
        'name': 'Scary', 
        'danger': 'Will kill you within 24 hours. Call 000.  NOW!', 
        'image': url_for("images", filename='Scary'),
        'uploaded': request.files['image'].read()
    }

    return render_template("result.html", info=info)


app.run(host='0.0.0.0', debug=True, threaded=True)
