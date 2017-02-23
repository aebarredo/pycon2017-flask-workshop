from myapp import app

if __name__ == '__main__':

    app.run(host=app.config['BIND_IP'],
            port=app.config['BIND_PORT'],
            debug=app.config['DEBUG'])
