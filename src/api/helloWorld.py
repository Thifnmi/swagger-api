import logging
import sys
from flask import request
from src.api import bp
from marshmallow import Schema, fields


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@bp.route("/hello")
def hello():
    """Get hello
        ---
        get:
            description: get hello
            response:
                200:
                    description: helloworld
                    content:
                        application/json:
                            schema
    """
    return "Wellcome get event!!"