import json

from flask import Flask, url_for, request, make_response

app = Flask(__name__)
app.config.from_object('config')


@app.route('/info', methods=['POST'])
def info():
    print(request.headers)

    app_shortname = request.headers.get('x-app-shortname')
    basic_authentication = request.headers.get('Authorization')
    print('App shortname {}, authentication {}'.format(app_shortname, basic_authentication))

    # you can parse basic authentication using base64
    # or you can just access request.authorization

    if request.authorization is not None:
        username = request.authorization.username
        password = request.authorization.password

        print('Username {}, password {}'.format(username, password))

    return ""


@app.route('/info2', methods=['POST', 'GET'])
def info2():

    print(request.args)

    param1 = request.args.get('param1')
    param2 = request.args.get('param2')

    print('param1 = {}, param2 = {}'.format(param1, param2))
    print(request.data)

    retval = {}

    http_stat = 200
    retval['status'] = 'SUCCESS'
    
    if request.method == 'POST':
        data = request.data
        json_data = json.loads(data)
        print(json_data)

        param3 = json_data.get('param3', None)
        param4 = json_data.get('param4', None)

        if param3 is None or param4 is None:
            http_stat = 400
            retval['status'] = 'FAIL'

    resp = make_response(json.dumps(retval), http_stat)
    resp.headers['Content-Type'] = 'application/json'

    return resp