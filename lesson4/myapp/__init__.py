import json

from flask import Flask, request
from flask_restful import Api

from .controllers import InfoHandler, InfoHandlerV2

app = Flask(__name__)
app.config.from_object('config')

# Flask restful API init
api = Api(app)

api.add_resource(InfoHandler, '/v1/info')

# what happens if endpoint name is not specified?
api.add_resource(InfoHandlerV2, '/v2/info', endpoint='v2_info1')
api.add_resource(InfoHandlerV2, '/v2/info/<id>', endpoint='v2_info2')