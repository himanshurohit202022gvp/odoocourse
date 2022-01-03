from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal

class Mycontroller(portal.CustomerPortal):
    # @http.route('/estate/index', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"


    # @http.route('/estate/index', auth='public')
    # def list(self, **kw):
    #         return http.request.render('estate.index', {
    #             'names':['abc','def','xyz'],
    #             'city':['ahm','gandh','brd']
            
    #     })

     @http.route('/estate/property', auth='user',website=True)
     def list(self, **kw):
            estate=http.request.env['estate.property']
            return http.request.render('estate.index', {
                'properties':estate.search([])
        })


     def _prepare_home_portal_values(self, counters):
         values =  super()._prepare_home_portal_values(counters)
         Properties = request.env['estate.property']
         values['total_properties'] = Properties.search_count([]) or 0
         return values


     @http.route('/my/properties',auth='user',website=True)
     def my_properties(self,**kw):
         estate = request.env['estate.property'].search([])
         values = self._prepare_portal_layout_values()
         values.update({
            'properties':estate,
            'page_name':'my_properties',})

         return http.request.render('estate.portal_my_properties',values)