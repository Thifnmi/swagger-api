import os
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from conf import config, get_logger
from src import create_app


logger = get_logger()


def serve():
    env = os.getenv("ENV", "development")

    if config[env].SENTRY_DSN:
        sentry_logging = LoggingIntegration(
            level=logging.info,
            event_level=logging.ERROR,
        )
        sentry_sdk.init(
            dsn=config[env].SENTRY_DSN,
            integrations=[sentry_logging],
            traces_sample_rate=1.0,
        )

    app = create_app()
    app.run(host=config[env].HOST, port=config[env].PORT)


if __name__ == "__main__":
    serve()
