from odoo import models
from odoo import Command

class EstateProperty(models.Model):
    _inherit="estate.property"

    def action_sold_property(self):
        for record in self:
            self.env['account.move'].create(
                {
                    "partner_id": self.buyer_id.id,
                    "move_type": "out_invoice",
                    "line_ids": [
                        Command.create({
                            "name": "6% of the selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06
                        }),
                        Command.create({
                            "name": "An additional 100.00 from administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00
                        })
                    ]
                }
            )
        return super().action_sold_property()