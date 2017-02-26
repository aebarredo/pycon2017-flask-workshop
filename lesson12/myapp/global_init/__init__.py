from .flask_app import create_flask_app
from .dbsession import setup_db_session
from .logger import setup_logger
from .limiter import setup_limiter
from .task_q import make_celery

app = create_flask_app()
Session = setup_db_session(app)
logger = setup_logger(app)
limiter = setup_limiter(app)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)
