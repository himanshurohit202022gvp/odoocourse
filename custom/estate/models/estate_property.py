
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError



class Test(models.Model):
    _name='test'
    _description = 'Test'
    # _rec_name = data

    data = fields.Char()
    pincode = fields.Integer()

    # seld here will be recordset [ list of many records ]
    def name_get(self):
        res = []
        for r in self:
            res.append((r.id, r.data))
        return res

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'),('refuse', 'Refused')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    def action_accepted(self):
        # Open the view only if we find the duplicate price or same price
        for record in self:
            # record.price
            same_price = []
            for rec in record.property_id.property_offer_ids:
                if rec.price == record.price and rec.id != record.id:
                    same_price.append(rec)

            if same_price:
                # view_id = self.env.ref('estate.estate_property_offer_tree').id
                partner_ids = [record.partner_id.id]
                for r in same_price:
                    partner_ids.append(r.partner_id.id)
                return {
                    "name": "Confirm Accept",
                    "type": "ir.actions.act_window",
                    "res_model": "confirm.accept",
                    "views": [[False, 'form']],
                    # "res_id": 2,
                    "target": "new",
                    "context" : {'default_selected_partner_id' : record.partner_id.id, 'partners': partner_ids},
                    "domain": [('selected_partner_id', 'in', partner_ids)]
                }
            else:
                pass


        # for record in self:
        #     # Do something to change status of other properties as rejected
        #     for rec in record.property_id.property_offer_ids:
        #         rec.status = 'refuse'
        #
        #     record.status = 'accepted'
        #     # Set Buyer and selling price
        #     record.property_id.selling_price = record.price
        #     record.property_id.buyer_id = record.partner_id


    def action_refused(self):
        for record in self:
            record.status = 'refuse'


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [('unique_property_tag_name', 'unique(name)', 'Tag cannot be duplicated')]

    name = fields.Char()
    color = fields.Integer()


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'Type cannot be duplicated')]

    name = fields.Char()
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count =  len(record.offer_ids)



class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit ='portal.mixin'
    _description = 'Estate Property'
    _sql_constraints = [('postive_price', 'check(expected_price >0)', 'Enter positive value')]
    _order = "id desc"
    
    # def test(self):
    #     return fields.Datetime.now()

    ref_seq = fields.Char(string="Reference ID",default="New")
    name = fields.Char(string="Title", default="Unknown", required=True)
    owner_id  = fields.Many2one('res.partner')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Datetime.now(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')        
        ])
    active = fields.Boolean(default=True)
    image = fields.Image()
    property_type_id = fields.Many2one('estate.property.type')
    salesman_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')
    test_id = fields.Many2one('test')
    property_tag_ids = fields.Many2many('estate.property.tag')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute="_compute_area", inverse="_inverse_area")
    best_price = fields.Float(compute="_compute_best_price", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)


    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability, days=record.validity)
            # date_availability


    @api.depends('property_offer_ids.price')
    def _compute_best_price(self): # Recordset [ Collection  of records]
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        print("\n\n ----- _compute_area method call")
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2

    def action_sold(self):
        # print("\n\n In action sold")
        for record in self:
            if record.state=='cancel':
                raise UserError("Cancel Property cannot be sold")
            record.state = 'sold'
            # return some action 

    def action_cancel(self):
        for record in self:
            if record.state=='sold':
                raise UserError("Sold Property cannot be canceled")
            record.state = 'cancel'

    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")


    def open_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
        }

    # Overriding methods
    @api.model
    def create(self, vals):
        # vals is a dict of all fields with values or default values  -> insert
        # vals['name'] = uppercase
        print("\n Create method is called ", vals)
        # vals['ref_seq'] = "Prop/123"
        if vals.get('ref_seq', 'New') == 'New':
            vals['ref_seq'] = self.env['ir.sequence'].next_by_code('property.seq')

        t =  super(EstateProperty, self).create(vals)
        return t

    def write(self, vals):
        # dict of changed field -> update
        print("\n Write method is called ", vals)
        return super(EstateProperty, self).write(vals)

    def compute_access_url(self):
        super()._compute_access_url()
        for record in self:
            record.compute_access_url = '/my/property/%s' %(record.id)

        # Change -> Super
        # Super -> Do something

class ResCongigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    my_select = fields.Selection([('1', 'One'), ('2', 'Two')])