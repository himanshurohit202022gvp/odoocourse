{
    'name': 'esate',
    'category' : 'Sales',
    'application' : True,
    'depends':['account'],
    'data':[
            'security/access_security.xml',
           'security/ir.model.access.csv',
           'views/estate_menus.xml',
           'views/estate_property_views.xml',
           'report/property_report.xml',
           'report/property_detail.xml',
           'wizard/print_report_view.xml',
           'wizard/create_sold_invoice_view.xml',
           'wizard/confirm_accept_view.xml',
    ],
   
}
