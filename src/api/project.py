import logging
import sys
from src.api import bp
from src.schema.error_schema import *
from src.schema.project_schema import *
from src.schema.taskEvent_schema import *
from src.schema.user_schema import *
from flask import jsonify, request


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@bp.route('/projects')
def listProject():
    """Get List of project
    ---
    get:
        summary: get list of project
        tags:
            - Projects
        parameters:
            -   name: all
                in: query
                schema:
                    type: string
                description: allow list all projects without pagination
            -   name: email
                in: query
                schema:
                    type: string
                description: filter based on email 
            -   name: user_uuid
                in: query
                schema:
                    type: string
                    format: uuid
            -   name: role
                in: query
                schema:
                    type: string
                    enum: [all, Owner, Member, Maintainer, Reader]
                required: true
                description: filter based on role 
            -   name: project_name
                in: query
                schema:
                    type: string
                description: filter based on project name 
            -   name: project_uuid
                in: query
                schema:
                    type: string
                description: filter based on project id
            -   name: project_alias_name
                in: query
                schema:
                    type: string
                description: filter based on project alias name
            -   name: sort
                in: query
                schema:
                    type: string
                enum: [asc, desc]
                description: >
                    Sort order:
                        * `project_name:asc` - Ascending, from A to Z
                        * `project_name:desc` - Descending, from Z to A
                        * `created_at:asc` - Ascending, from A to Z
                        * `created_at:desc` - Descending, from Z to A
            -   name: limit
                in: query
                description: How many items to return at one time (max 100)
                required: false
                schema:
                    type: integer
                    format: int32
            -   name: page
                in: query
                description: specific page that reach to
                required: false
                schema:
                    type: integer
                    format: int32
            -   name: offset
                in: query
                description: specific size page that want
                required: false
                schema:
                    type: integer
                    format: int32
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

    response = [
        {
            "success": boolean(1),
            "message": "List project success",
            "error_code": 0,
            "data": [{
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
                }],
            "metadata": {
                "total": 100,
                "current_page": 1,
                "has_next": boolean(0),
                "has_previous": 1,
                "previous_page": 1,
                "next_page": 1
            }
        }
    ]

    return jsonify(response)

@bp.route('/project/create', methods=["POST"])
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
                schema:
                    type: string 
        responses:
            200:
                description: Task event info
                content:
                    application/json:
                        schema: TaskEventCreateProject
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

    payload = {
        "user_uuid": request.headers.get("user_uuid"),
        "user_email": request.headers.get("user_email"),
        "project_name": request.headers.get("project_name"),
        "description": request.headers.get("user_uuid")
    }

    response = [
        {
            "task_event": {
                'task_event_id': 1,
                'status': 'success',
                'type': 'create'
            }
        }, {
        'project': payload
    }]

    return jsonify(response)

@bp.route('/project/<project_uuid>')
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

    response = [{
        'uuid': project_uuid,
        'origin_name': 'project1',
        'alias_name': "day la project 1",
        'description': "day la description project 1",
        'role': "owner"
    }]

    return jsonify(response)

@bp.route('/project/<project_uuid>/users')
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
            -   name: all
                in: query
                schema:
                    type: string
                description: allow list all users without pagination
            -   name: username
                in: query
                schema:
                    type: string
                description: filter based on username 
            -   name: group_name
                in: query
                schema:
                    type: string
                    format: uuid
                description: filter based on group_name 
            -   name: sort
                in: query
                schema:
                    type: string
                enum: [asc, desc]
                description: >
                    Sort order:
                        * `user_name:asc` - Ascending, from A to Z
                        * `user_name:desc` - Descending, from Z to A
                        * `created_at:asc` - Ascending, from A to Z
                        * `created_at:desc` - Descending, from Z to A
            -   name: limit
                in: query
                description: How many items to return at one time (max 100)
                required: false
                schema:
                    type: integer
                    format: int32
            -   name: page
                in: query
                description: specific page that reach to
                required: false
                schema:
                    type: integer
                    format: int32
            -   name: offset
                in: query
                description: specific size page that want
                required: false
                schema:
                    type: integer
                    format: int32 
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

    response = [
        {
            "success": boolean(1),
            "message": "List user in project %s success",
            "error_code": 0,
            "project": {
                        'uuid': '1',
                        'origin_name': 'project1',
                        'alias_name': "day la project 1",
                        'description': "day la description project 1",
                        'role': "owner"
                    },
            "data": [{
                        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f25',
                        'user_email': 'test@gmail.com',
                        'description': "user full permission",
                        'role': "owner",
                        'is_active': boolean(1),
                        'created_at': '2022-04-21T02:30:28.911Z'
                    }, {
                        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f26',
                        'user_email': 'test1@gmail.com',
                        'description': "day la description project 1",
                        'role': "admin",
                        'is_active': boolean(1),
                        'created_at': '2022-04-21T02:30:28.911Z'
                    },{
                        'uuid': 'b0a6dc1e-dda8-4562-b62c-007bb7993f27',
                        'user_email': 'test@gmail.com',
                        'description': "day la role custom",
                        'role': "dev",
                        'is_active': boolean(1),
                        'created_at': '2022-04-21T02:30:28.911Z'
                    }],
            "metadata": {
                "total": 100,
                "current_page": 1,
                "has_next": boolean(0),
                "has_previous": 1,
                "previous_page": 1,
                "next_page": 1
            }
        }
    ]

    return jsonify(response)

@bp.route('/project/update/<project_uuid>', methods=['PUT'])
def updateProject(project_uuid):
    """Get info project
    ---
    put:
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
            -   name: project_name
                in: header
                description: project name user want create
                required: true
                schema:
                    type: string
            -   name: description
                in: header
                description: description of project
                schema:
                    type: string 
        responses:
            200:
                description: info project
                content:
                    application/json:
                        schema: TaskEventUpdateProject
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
    payload = {
        "project_name": request.headers.get("project_name"),
        "description": request.headers.get("description")
    }
    before_values = {
        'project_name': 'project1',
        'description': "day la description project 1"
    }
    response = [{
        "task_event": {
            'task_event_id': 2,
            'status': 'success',
            'type': 'update'
        }
    }, {
        "project": {
            "before_values": before_values,
            "after_values": payload
        }
    }]

    return jsonify(response)

@bp.route('/project/delete/<project_uuid>', methods=['DELETE'])
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
        responses:
            200:
                description: delete project
                content:
                    application/json:
                        schema: TaskEventDeleteProject
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

    project = {
        'project_name': 'project1',
        'description': "day la description project 1"
    }

    response = [
        {
            "task_event": {
                'task_event_id': 3,
                'status': 'success',
                'type': 'delete'
            }
        }, {
            "project": project
            }
    ]

    return jsonify(response)