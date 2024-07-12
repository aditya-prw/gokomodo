import json

from odoo import api, fields, models, _


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    business_model = fields.Selection(
        [('rt', 'Retail'), ('corp', 'Corporate'), ('sub', 'Subscription')],
        string="Business Model", required=True, index=True, default='rt'
    )
    display_name = fields.Char(
        "Name", compute="_compute_display_name", store=True)

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            if rec.business_model == 'rt':
                name = f'[RT] — {rec.name}'
            elif rec.business_model == 'corp':
                name = f'[CORP] — {rec.name}'
            elif rec.business_model == 'sub':
                name = f'[SUB] — {rec.name}'
            else:
                name = rec.name
            res.append((rec.id, name))
        return res

    def _compute_display_name(self):
        for rec in self:
            if rec.business_model == 'rt':
                rec.display_name = f'[RT] — {rec.name}'
            elif rec.business_model == 'corp':
                rec.display_name = f'[CORP] — {rec.name}'
            elif rec.business_model == 'sub':
                rec.display_name = f'[SUB] — {rec.name}'
            else:
                rec.display_name = rec.name


class CustomSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tax_id_domain = fields.Char(
        compute='_compute_taxes_domain',
        readonly=True,
        store=False,
    )
    #
    @api.multi
    @api.depends('order_id.business_model')
    def _compute_taxes_domain(self):
        for rec in self:
            rec.tax_id_domain = rec.get_tax_id_domain()
        return True

    def get_tax_id_domain(self):
        domain = [('business_model', '=', getattr(self.order_id, 'business_model', '')), ('type_tax_use', '=', 'sale'),
                  ('company_id', '=', self.order_id.company_id.id)]
        return json.dumps(domain)
