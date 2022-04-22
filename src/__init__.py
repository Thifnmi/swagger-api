import os
import yaml
from flask import Flask, jsonify
from conf import config
from apispec import APISpec
from apispec.utils import validate_spec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory

from src.api.taskEventId import listTaskEvent


env = os.getenv("ENV", "development")

def create_app():
    app = Flask(__name__, template_folder='../swagger/templates')
    app.config['JSON_SORT_KEYS'] = False
    app.config["BASE_URL"] = "/api/iam/v2/"
    OPENAPI_SPEC = """
        servers:
        - url: http://127.0.0.1:9997/
        - url: https://staging2.bizflycloud.vn/api/iam/v2
        - url: https://manage.bizflycloud.vn/api/iam/v2
        - url: https://dev.bizflycloud.vn/api/iam/v2
    """

    settings = yaml.safe_load(OPENAPI_SPEC)
    spec = APISpec(
        title='OpenAPI for iam v2 public api',
        version='1.0.0',
        openapi_version='3.0.2',
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        **settings
    )
    validate_spec(spec)
    @app.route('/')
    def introduce():
        return jsonify({
            "auth": "Thifnmi",
            "full name": "Tu Van Thin",
            "email": {
                "personal": "tuthin2k@gmail.com",
                "VCCorp": "thintuvan@vccorp.vn",
                "VCCloud": "thintv@vccloud.vn"
            },
            "telegram": "@Thifnmi"
        })

    @app.route('/api-docs')
    def api_docs():
        return jsonify(spec.to_dict())

    from src.api import bp
    app.register_blueprint(bp)

    from src.api.project import listProject, getProject, getUserProject, updateProject, deleteProject, createProject
    from src.api.healthCheck import healthCheck
    from src.api.taskEventId import getTaskEvent

    with app.test_request_context():
        spec.path(view=healthCheck)
        spec.path(view=getTaskEvent)
        spec.path(view=listTaskEvent)
        spec.path(view=listProject)
        spec.path(view=getProject)
        spec.path(view=getUserProject)
        spec.path(view=createProject)
        spec.path(view=updateProject)
        spec.path(view=deleteProject)

    @app.route('/docs')
    @app.route('/docs/<path:path>')
    @app.route('/<path:uri>/docs/<path:path>')
    def swagger_docs(uri=None, path=None):
        if not path or path == 'index.html':
            if uri == None:
                return render_template('index.html', base_url=f"/docs")
            else:
                return render_template('index.html', base_url=f"{uri}/docs")
        else:
            return send_from_directory('../swagger/static', path)
    return app
