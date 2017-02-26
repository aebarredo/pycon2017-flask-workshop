from .flask_app import create_flask_app
from .dbsession import setup_db_session
from .logger import setup_logger
from .limiter import setup_limiter

app = create_flask_app()
Session = setup_db_session(app)
logger = setup_logger(app)
limiter = setup_limiter(app)

