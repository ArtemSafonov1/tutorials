from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type description"
    _order = "sequence, name"

    name = fields.Char(
        required=True
    )

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )

    sequence = fields.Integer('Sequence', default=1, help="Used to order types")

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )

    offer_count = fields.Integer(
        string="Offer count",
        compute="_compute_offer_count"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)