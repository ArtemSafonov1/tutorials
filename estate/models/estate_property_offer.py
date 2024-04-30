from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer description"
    _order = "price desc"

    _sql_constraints = [
        ('price', 'CHECK(price > 0)', 'The price must be strictly positive.')
    ]

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'), ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            property = record.property_id
            property.selling_price = record.price
            property.buyer_id = record.partner_id
            property.state = 'offer_accepted'
            other_offers = property.offer_ids.search([('id', '!=', record.id)])
            for offer in other_offers:
                offer.status = 'refused'
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                record.property_id.state = "offer_received"
            record.status = 'refused'
        return True
