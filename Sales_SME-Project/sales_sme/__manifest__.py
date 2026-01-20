{
    'name': "Sales SME",
    'version': '19.1.0.1.1',
    'author': "Mohamed Yasser",
    'category': 'Tools',
    'depends': ['base', 'contacts', 'product', 'mail', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sales_order_view.xml',
        'views/sale_order_view.xml',
        'views/product_template_view.xml',
        'wizard/sale_order_reject_view.xml',
        'security/security.xml',
        'reports/product_report.xml',
    ],
    'assets':{
        'web.assets_backend': [
            'sales_sme/static/src/components/productMatrixViews/productMatrixView.js',
            'sales_sme\static\src\components\productMatrixViews\productMatrixView.xml'
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
