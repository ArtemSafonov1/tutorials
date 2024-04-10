from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag description"

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'The name must be unique.')
    ]

    name = fields.Char(
        required=True
    )
