from marshmallow import Schema, fields


class ProjectResponseSchema(Schema):
    uuid = fields.Str()
    origin_name = fields.Str()
    alias_name = fields.Str()
    description = fields.Str()
    role = fields.Str()

class ProjectListResponseSchema(Schema):
    project_list = fields.List(fields.Nested(ProjectResponseSchema))