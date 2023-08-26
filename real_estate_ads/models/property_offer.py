from odoo import fields, models, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string="Description", compute=_compute_name)
    price = fields.Monetary(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    partner_email = fields.Char(string="Customer Email", related='partner_id.email')
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    currency_id = fields.Many2one("res.currency", string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Create Date", default=_set_create_date)

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline cannot be before creation date"))

    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })
        self.status = 'accepted'

    def _validate_accepted_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if offer_ids:
            raise ValidationError("You have an accepted offer already")

    def action_decline_offer(self):
        self.status = 'refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    def extend_offer_deadline(self):
        activ_ids = self._context.get('active_ids', [])
        if activ_ids:
            offer_ids = self.env['estate.property.offer'].browse(activ_ids)
            for offer in offer_ids:
                offer.validity = 10

    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity = offer.validity + 1