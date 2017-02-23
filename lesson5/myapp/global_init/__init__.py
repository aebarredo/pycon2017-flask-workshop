from .flask_app import create_flask_app
from .dbsession import setup_db_session

app = create_flask_app()
Session = setup_db_session(app)

