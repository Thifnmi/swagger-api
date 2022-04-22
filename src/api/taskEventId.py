from src.api import bp
from src.schema.error_schema import *
from src.schema.project_schema import *
from src.schema.taskEvent_schema import *
from src.schema.user_schema import *
from flask import jsonify


@bp.route('/task-event/<project_uuid>')
def listTaskEvent(project_uuid):
    """List task event info
    ---
    get:
        summary: List task event info
        tags:
            - Task Event
        description: List task event info
        parameters:
            -   name: project_uuid
                in: header
                description: uuid of project
                required: true
                schema:
                    type: string
        responses:
            200:
                description: List task event of project %s
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

    if project_uuid:
        listTaskEvent = [{
                "task_event_id": 1,
                "status": "pending",
                "type": "create"
            }, {
                "task_event_id": 2,
                "status": "pending",
                "type": "update"
            }, {
                "task_event_id": 3,
                "status": "success",
                "type": "create"
            }, {
                "task_event_id": 9,
                "status": "pending",
                "type": "delete"
            }]

    return jsonify(listTaskEvent)

@bp.route('/task-event/<task_event_id>')
def getTaskEvent(task_event_id):
    """Get result task event info
    ---
    get:
        summary: Get result task event info
        tags:
            - Task Event
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

    if int(task_event_id) == 1:
        taskEvent = {
            'task_event_id': int(task_event_id),
            'status': 'success',
            'type': "create"
        }
    elif int(task_event_id) == 2:
        taskEvent = {
            'task_event_id': int(task_event_id),
            'status': 'success',
            'type': "update"
        }
    elif int(task_event_id) == 3:
        taskEvent = {
            'task_event_id': int(task_event_id),
            'status': 'success',
            'type': "delete"
        }

    return jsonify(taskEvent)
