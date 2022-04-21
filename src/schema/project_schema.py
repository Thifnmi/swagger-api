from marshmallow import Schema, fields
from .utils import *


class ProjectResponseSchema(Schema):
    uuid = fields.Str()
    origin_name = fields.Str()
    alias_name = fields.Str()
    description = fields.Str()
    role = fields.Str()

class ProjectListResponseSchema(Schema):
    success = fields.Boolean()
    message = fields.Str()
    error_code = fields.Int()
    data = fields.List(fields.Nested(ProjectResponseSchema))
    metadata = fields.Nested(Metadata)