import logging
import sys
from xmlrpc.client import boolean
from src.api import bp
from src.schema.error_schema import *
from src.schema.healthCheck_schema import *
from flask import jsonify


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@bp.route('/v2/healthcheck')
def healthCheck():
    """Get healthcheck service
    ---
    get:
        summary: Get healthcheck service
        tags:
            - Healthcheck
        description: Get healthcheck service
        responses:
            200:
                description: Healthcheck service
                content:
                    application/json:
                        schema: HealthCheck
            500:
                description: Server Error
                content:
                    application/json:
                        schema: ServerError
            default:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: DefaultError
    """

    response = {
        'success': boolean(1),
        'error_code': 0,
        'message': "healthy"
    }

    return jsonify(response)