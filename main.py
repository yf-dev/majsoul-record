import logging
from flask import Flask

from src.apis import bp as api_bp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Flask(__name__)
app.register_blueprint(api_bp)
