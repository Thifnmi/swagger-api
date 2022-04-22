from marshmallow import Schema, fields


class TaskEvent(Schema):
    task_event_id = fields.Str()
    type = fields.Str()
    status = fields.Str()


class PayloadCreateProject(Schema):
    user_uuid = fields.Str()
    user_email = fields.Str()
    project_name = fields.Str()
    description = fields.Str()

class ValuesProject(Schema):
    project_name = fields.Str()
    description = fields.Str()

class TaskEventCreateProject(Schema):
    task_event = fields.Nested(TaskEvent)
    project = fields.Nested(PayloadCreateProject)

class ValuesUpdate(Schema):
    before_values = fields.Nested(ValuesProject)
    after_values = fields.Nested(ValuesProject)
class TaskEventUpdateProject(Schema):
    task_event = fields.Nested(TaskEvent)
    project = fields.Nested(ValuesUpdate)

class TaskEventDeleteProject(Schema):
    task_event = fields.Nested(TaskEvent)
    project = fields.Nested(ValuesProject)