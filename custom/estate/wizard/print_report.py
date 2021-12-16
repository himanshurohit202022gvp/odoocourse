
from odoo import fields, models

class PrintReport(models.TransientModel):
    _name = 'print.report'
    _description = 'Print Report'

    amount = fields.Integer("Enter Amount", default=10000)

    def print(self):
        print("\n\nPrint report ")
        # Call the report to display data 
        # We want to pass this amount and add logic in current report to 
        # display all properties where expected price is greated than 10000
        # docs : documets for the report 
        """
        create a docs of [ records of some model ] for o in docs
        x = [1] 1 
        x [1,2]
        """

        # Comditon -> triplets in tuple docs
        # ('a', '>', 'b') --> a > b and a > c 
        # .search(['|',('a', '>', 'b'), ('a', '>', 'c')]) ==> and 


        docs = self.env['estate.property'].search([('expected_price', '>=', self.amount)]).ids
        # t = self.env['estate.property'].browse(docs)


        return self.env.ref('estate.report_print_property').report_action(docs)