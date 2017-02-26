from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def setup_limiter(app):

    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)

    return limiter
