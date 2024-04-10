from odoo import api, fields, models

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
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            if len(prices) > 0:
                record.best_price = max(prices)
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None