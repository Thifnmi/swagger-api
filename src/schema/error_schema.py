from xmlrpc.client import boolean
from marshmallow import Schema, fields

class DefaultError(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
    data = fields.Str()

class UnauthorizedError(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()

class PermissionDeny(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()

class PageNotFound(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()

class StatusExpectationFailed(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()

class ServerError(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
