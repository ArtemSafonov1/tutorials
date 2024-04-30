from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property description"
    _order = "id desc"

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

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
        help="Orientation is used to choose garden orientation"
    )
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
        readonly=True,
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

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        for record in self:
            if record.state == "new" and len(record.offer_ids) > 0:
                record.state = "offer_received"
            elif len(record.offer_ids) == 0:
                record.state = "new"

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_('Canceled properties can not be sold.'))
            else:
                record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Sold properties can not be canceled.'))
            else:
                record.state = 'canceled'
        return True

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.expected_price * 0.9, record.selling_price, 2) > 0:
                raise ValidationError(_('The selling price must be at least 90% of the expected price. You must reduce the expected price if you want to accept this offer.'))