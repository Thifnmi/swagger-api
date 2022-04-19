# import os
# import logging
# import sentry_sdk
# from sentry_sdk.integrations.logging import LoggingIntegration
# from conf import config, get_logger
# from src import create_app

# logger = get_logger()


# def serve():
#     env = os.getenv("ENV", "development")

#     if config[env].SENTRY_DSN:
#         sentry_logging = LoggingIntegration(
#             level=logging.info,
#             event_level=logging.ERROR,
#         )
#         sentry_sdk.init(
#             dsn=config[env].SENTRY_DSN,
#             integrations=[sentry_logging],
#             traces_sample_rate=1.0,
#         )

#     app = create_app()
#     app.run(host=config[env].HOST, port=config[env].PORT)


# if __name__ == "__main__":
#     serve()
import yaml
from apispec import APISpec
from apispec.utils import validate_spec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory
from marshmallow import Schema, fields

app = Flask(__name__, template_folder='swagger/templates')


@app.route('/')
def hello_world():
    return 'Hello, World'

OPENAPI_SPEC = """
openapi: 3.0.2
servers:
- url: http://127.0.0.1:9999/
- url: https://staging.bizflycloud.vn/api/iam_v2
- url: https://manage.bizflycloud.vn/api/iam_v2
- url: https://dev.bizflycloud.vn/api/iam_v2
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

@app.route('/api-docs')
def create_swagger_spec():
    return jsonify(spec.to_dict())


class ProjectResponseSchema(Schema):
    uuid = fields.Str()
    origin_name = fields.Str()
    alias_name = fields.Str()
    description = fields.Str()
    role = fields.Str()

class ProjectListResponseSchema(Schema):
    project_list = fields.List(fields.Nested(ProjectResponseSchema))

class DefaultError(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
    data = fields.Str()

class PermissionDeny(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
    data = fields.Str()

class PageNotFound(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
    data = fields.Str()

class StatusExpectationFailed(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
    data = fields.Str()

class ServerError(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
    data = fields.Str()

@app.route('/projects')
def listProject():
    """Get List of project
    ---
    get:
        summary: get list of project
        tags:
            - project
        description: Get List of project
        responses:
            200:
                description: list project
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }, {
        'uuid': '0bea2c68-01eb-43c1-8fc8-bacfefb6f63d',
        'origin_name': "project2",
        'alias_name': "cai nay to lam",
        'description': "",
        'role': "admin"
    }]

    return ProjectListResponseSchema().dump({'project_list': response})

@app.route('/project/create')
def createProject(gist_id):
    """create project
    ---
    post:
        summary: create project
        tags:
            - project
        description: create project
        responses:
            200:
                description: Return a todo list
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False
    }, {
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]

    return ProjectListResponseSchema().dump({'todo_list': dummy_data})

@app.route('/project/create/<task_event_id>')
def getCreateProject(task_event_id):
    """Get task event create project info
    ---
    get:
        summary: Get task event create project info
        tags:
            - project
        description: Get task event create project info
        responses:
            200:
                description: info task event create project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return ProjectResponseSchema().dump({'project': response})

@app.route('/project/<project_uuid>')
def getProject(project_uuid):
    """Get info project
    ---
    get:
        summary: get info project
        tags:
            - project
        description: Get info project
        responses:
            200:
                description: info project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return ProjectResponseSchema().dump({'project': response})

@app.route('/project/update/<project_uuid>')
def updateProject(project_uuid):
    """Get info project
    ---
    put:
        summary: get info project
        tags:
            - project
        description: Get info project
        responses:
            200:
                description: info project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return ProjectResponseSchema().dump({'project': response})

    spec.path(view=listProject)
    spec.path(view=getProject)
    spec.path(view=createProject)
    spec.path(view=todo3)

@app.route('/project/update/<task_event_id>')
def getUpdateProject(task_event_id):
    """Get task event update project info
    ---
    get:
        summary: Get task event update project info
        tags:
            - project
        description: Get task event update project info
        responses:
            200:
                description: info task event update project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return ProjectResponseSchema().dump({'project': response})

@app.route('/project/delete/<project_uuid>')
def deleteProject(project_uuid):
    """Get info project
    ---
    delete:
        summary: get info project
        tags:
            - project
        description: Get info project
        responses:
            200:
                description: delete project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return ProjectResponseSchema().dump({'project': response})

@app.route('/project/delete/<task_event_id>')
def getDeleteProject(task_event_id):
    """Get task event delete project info
    ---
    get:
        summary: Get task event delete project info
        tags:
            - project
        description: Get task event delete project info
        responses:
            200:
                description: info task event delete project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                content:
                    application/json:
                        schema: ProjectListResponseSchema
            403:
                description: Permission Deny
                content:
                    application/json:
                        schema: PermissionDeny
            404:
                description: Page Notfound
                content:
                    application/json:
                        schema: PageNotFound
            417:
                description: Status Expectation Failed
                content:
                    application/json:
                        schema: StatusExpectationFailed
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

    response = [{
        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return ProjectResponseSchema().dump({'project': response})

with app.test_request_context():
    spec.path(view=listProject)
    spec.path(view=getProject)
    spec.path(view=createProject)
    spec.path(view=getCreateProject)
    spec.path(view=updateProject)
    spec.path(view=getUpdateProject)
    spec.path(view=deleteProject)
    spec.path(view=getDeleteProject)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)


if __name__ == '__main__':
    app.run(debug=True, port=9999)

