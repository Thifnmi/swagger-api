import os
from flask import Flask
from conf import config
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory
from marshmallow import Schema, fields

env = os.getenv("ENV", "development")

def create_app():
    app = Flask(__name__, template_folder='swagger/templates')

    @app.route('/')
    def hello_world():
        return 'Hello, World'

    spec = APISpec(
        title='OpenAPI for iam v2 public api',
        version='1.0.0',
        openapi_version='3.0.2',
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    @app.route('/api/swagger.json')
    def create_swagger_spec():
        return jsonify(spec.to_dict())


    class TodoResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        status = fields.Boolean()


    class TodoListResponseSchema(Schema):
        todo_list = fields.List(fields.Nested(TodoResponseSchema))


    @app.route('/todo')
    def todo():
        """Get List of Todo
        ---
        get:
            description: Get List of Todos
            responses:
                200:
                    description: Return a todo list
                    content:
                        application/json:
                            schema: TodoListResponseSchema
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

        return TodoListResponseSchema().dump({'todo_list': dummy_data})

    @app.route('/todo')
    def todo1():
        """Get List of Todo
        ---
        post:
            tag: admin
            description: Get List of Todos
            responses:
                200:
                    description: Return a todo list
                    content:
                        application/json:
                            schema: TodoListResponseSchema
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

        return TodoListResponseSchema().dump({'todo_list': dummy_data})


    with app.test_request_context():
        spec.path(view=todo)
        spec.path(view=todo1)

    @app.route('/docs')
    # @app.route('/docs/<path:path>')
    def swagger_docs(path=None):
        if not path or path == 'index.html':
            return render_template('./index.html', base_url='/docs')
        else:
            return send_from_directory('./swagger/static', path)


    return app
