import json

from odoo import api, fields, models, _


class CustomAccountTax(models.Model):
    _inherit = 'account.tax'

    business_model = fields.Selection(
        [('rt', 'Retail'), ('corp', 'Corporate'), ('sub', 'Subscription')],
        string="Business Model", required=True, index=True, default='rt'
    )
