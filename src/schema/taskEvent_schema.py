from marshmallow import Schema, fields


class TaskEvent(Schema):
    task_event_id = fields.Str()
    type = fields.Str()
    status = fields.Str()