###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_ids = fields.Many2many(
        string='Websites',
        comodel_name='website',
        relation='product_template2website_rel',
        column1='product_id',
        column2='website_id')

    def can_access_from_current_website(self, website_id=False):
        if not website_id:
            website_id = self.env['website'].get_current_website().id
        for product in self:
            if not product.website_ids:
                continue
            if website_id not in product.website_ids.ids:
                return False
        return True

class Website(models.Model):
    _inherit = 'website'

    def sale_product_domain(self):
        _logger.info('>>>>>>>')
        _logger.info(self.get_current_website().id)
        return ["|", "&"] + [("sale_ok", "=", True)] + [('website_ids', 'in', [self.sudo().get_current_website().id] )] + [('website_ids', '=', False )] + self.get_current_website().website_domain()
