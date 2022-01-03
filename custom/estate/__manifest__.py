{
    'name': 'Real Estate',
    'category' : 'Sales',
    'application' : True,
    'depends': ['base','account','website'],
    'data':[
        'data/seq.xml',
        'security/access_security.xml',
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'wizard/create_sold_invoice_view.xml',
        'wizard/confirm_accept_view.xml',
        'wizard/print_report_view.xml',
        'views/estate_property_views.xml',
        'report/property_report.xml',
        'report/property_detail.xml',
        'report/property_doc.xml',
        'views/estate_index.xml',
        'views/estate_portal_view.xml',
    ],
   
}
