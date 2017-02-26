from myapp import app, celery

if __name__ == '__main__':

    app.run(host=app.config['BIND_IP'],
            port=app.config['BIND_PORT'],
            debug=app.config['DEBUG'])
