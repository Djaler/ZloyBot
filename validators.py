from marshmallow import Schema, fields


class ReactionSchema(Schema):
    reactions = fields.List(fields.String(), required=True)
    triggers = fields.List(fields.String(), missing=None)
    chance = fields.Float(missing=100)
    is_reply_to_bot = fields.Boolean(missing=False)
