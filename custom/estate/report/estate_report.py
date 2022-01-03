
from odoo import models, fields, tools

class EstateReport(models.Model):
    _name = 'estate.report'
    _description = 'Estate Report'
    _auto = False # Dont create the table in database
    _rec_name = 'id'

    id = fields.Integer()
    offer_status = fields.Selection([('accepted', 'Accepted'),('refuse', 'Refused')])
    property_id = fields.Many2one('estate.property')
    property_state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new')
    property_type_id = fields.Many2one('estate.property_type')


    def _select(self):
        return """
            epo.id as id,
            epo.status as offer_status,
            epo.property_id as property_id,
            ep.state as property_state,
            ep.property_type_id as property_type_id
        """
    def _from(self):
        return """
        estate_property as ep join estate_property_offer as epo on epo.property_id = ep.id
        """

    def init(self):
        # PRovide what to do with this model -> create 
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""create or replace view %s as (
            select %s from %s)
            """ % (self._table, self._select(), self._from()))

    # select col1,col2,col3 from Table name