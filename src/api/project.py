import logging
import sys
from src.api import bp
from src.schema.error_schema import *
from src.schema.project_schema import *
from src.schema.taskEvent_schema import *
from src.schema.user_schema import *
from flask import jsonify


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@bp.route('/v2/projects')
def listProject():
    """Get List of project
    ---
    get:
        summary: get list of project
        tags:
            - Projects
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

    return jsonify({"list project": response})

@bp.route('/v2/project/create')
def createProject():
    """create project
    ---
    post:
        summary: create project
        tags:
            - Projects
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

    return TaskEvent().dump({'Task event': response})

@bp.route('/v2/project/<task_event_id>')
def getEventProject(task_event_id):
    """Get result task event info
    ---
    get:
        summary: Get result task event info
        tags:
            - Projects
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

@bp.route('/v2/project/<project_uuid>')
def getProject(project_uuid):
    """Get info project
    ---
    get:
        summary: get info project
        tags:
            - Projects
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
    print(1)
    if project_uuid:
        response = [{
            'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
            'origin_name': 'project1',
            'alias_name': "day la project 1",
            'description': "day la description project 1",
            'role': "owner"
        }]
    print(1)

    return ProjectResponseSchema().dump({'project': response})

@bp.route('/v2/project/<project_uuid>/users')
def getUserProject(project_uuid):
    """Get user of project
    ---
    get:
        summary: get user of project
        tags:
            - Projects
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

@bp.route('/v2/project/update/<project_uuid>')
def updateProject(project_uuid):
    """Get info project
    ---
    put:
        summary: get info project
        tags:
            - Projects
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

@bp.route('/v2/project/delete/<project_uuid>')
def deleteProject(project_uuid):
    """Delete project
    ---
    delete:
        summary: Delete project
        tags:
            - Projects
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