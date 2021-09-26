import typing as t

from flask import Flask

from src.apis import bp as api_bp


def create_app(test_config: t.Dict = None) -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    if test_config is not None:
        app.config.from_mapping(test_config)

    return app
