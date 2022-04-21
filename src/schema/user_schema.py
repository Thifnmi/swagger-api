from marshmallow import Schema, fields

from .project_schema import ProjectResponseSchema
from .utils import *

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
    success = fields.Boolean()
    message = fields.Str()
    error_code = fields.Int()
    project = fields.Nested(ProjectResponseSchema)
    data = fields.List(fields.Nested(UserOfProject))
    metadata = fields.Nested(Metadata)