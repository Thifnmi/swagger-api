from marshmallow import Schema, fields

class HealthCheck(Schema):
    success = fields.Boolean()
    error_code = fields.Int()
    message = fields.Str()
