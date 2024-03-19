from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property description"

    name = fields.Char(
        required=True
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(
        required=True
    )
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        default=2
    )
    living_area = fields.Integer(
        string="Living Area (sqm)"
    )
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(
        string="Garden Area (sqm)"
    )
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation is used to choose garden orientation")
    active = fields.Boolean(
        default=True
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'), ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')
        ],
        help="Choose state of property",
        default='new',
        required=True,
        copy=False
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Type",
        index=True
    )
    salesman_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        'res.partner',
        copy=False
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
