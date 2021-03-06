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
- url: http://127.0.0.1:9997/
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

class UnauthorizedError(Schema):
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

class TaskEvent(Schema):
    task_event_id = fields.Str()
    type = fields.Str()
    status = fields.Str()

class UserOfProject(Schema):
    uuid = fields.Str()
    user_email = fields.Str()
    description = fields.Str()
    user_role = fields.Str()
    is_active = fields.Boolean()
    created_date = fields.DateTime()

class ListUser(Schema):
    list_user = fields.List(fields.Nested(UserOfProject))

class ListUserOfProject(Schema):
    project = fields.Nested(ProjectResponseSchema)
    list_user = fields.List(fields.Nested(UserOfProject))

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
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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
def createProject():
    """create project
    ---
    post:
        summary: create project
        tags:
            - project
        description: create project
        parameters:
            -   name: user_uuid
                in: header
                description: UUID of user
                required: true
                schema:
                    type: string
            -   name: type
                in: header
                description: type of event
                required: true
                schema:
                    type: string 
            -   name: user_email
                in: header
                description: email of user
                required: true
                schema:
                    type: string 
            -   name: project_name
                in: header
                description: project name user want create
                required: true
                schema:
                    type: string 
            -   name: description
                in: header
                description: description of project
                required: true
                schema:
                    type: string 
        responses:
            200:
                description: Task event info
                content:
                    application/json:
                        schema: TaskEvent
            401:
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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
        'task_event_id': 1,
        'status': "created"
    }]

    return TaskEvent().dump({'todo_list': response})

@app.route('/project/<task_event_id>')
def getEventProject(task_event_id):
    """Get result task event info
    ---
    get:
        summary: Get result task event info
        tags:
            - project
        description: Get result task event info
        parameters:
            -   name: task_event_id
                in: header
                description: ID of task event
                required: true
                schema:
                    type: string
            -   name: type
                in: header
                description: type of event
                required: true
                schema:
                    type: string
        responses:
            200:
                description: task event info
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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
        parameters:
            -   name: project_uuid
                in: path
                description: UUID of project
                required: true
                schema:
                    type: string 
        responses:
            200:
                description: info project
                content:
                    application/json:
                        schema: ProjectResponseSchema
            401:
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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

@app.route('/project/<project_uuid>/users')
def getUserProject(project_uuid):
    """Get user of project
    ---
    get:
        summary: get user of project
        tags:
            - project
        description: Get user of project
        parameters:
            -   name: project_uuid
                in: path
                description: UUID of project
                required: true
                schema:
                    type: string 
        responses:
            200:
                description: List user of project
                content:
                    application/json:
                        schema: ListUserOfProject
            401:
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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
        parameters:
            -   name: user_uuid
                in: header
                description: UUID of user
                required: true
                schema:
                    type: string 
            -   name: project_name
                in: header
                description: project name user want create
                required: true
                schema:
                    type: string
            -   name: type
                in: header
                description: type of event
                required: true
                schema:
                    type: string 
            -   name: description
                in: header
                description: description of project
                required: true
                schema:
                    type: string 
        responses:
            200:
                description: info project
                content:
                    application/json:
                        schema: TaskEvent
            401:
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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
    """Delete project
    ---
    delete:
        summary: Delete project
        tags:
            - project
        description: Delete project
        parameters:
            -   name: project_uuid
                in: path
                description: UUID of project
                required: true
                schema:
                    type: string
            -   name: type
                in: header
                description: type of event
                required: true
                schema:
                    type: string 
        responses:
            200:
                description: delete project
                content:
                    application/json:
                        schema: TaskEvent
            401:
                description: Access token is missing or invalid
                content:
                    application/json:
                        schema: UnauthorizedError
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
    spec.path(view=getEventProject)
    spec.path(view=updateProject)
    spec.path(view=deleteProject)
    spec.path(view=getUserProject)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9997)
