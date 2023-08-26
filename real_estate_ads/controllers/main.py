from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route(['/properties'], type='http', website=True, auth="public")
    def show_properties(self):
        property_ids = request.env['estate.property'].sudo().search([])
        return request.render("real_estate_ads.property_list", {"property_ids": property_ids})