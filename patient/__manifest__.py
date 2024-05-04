{
    'name':'hospital',
    'author': 'sohila',
    'depends' : ['base','crm'],
    'data':[
                'security/res_group.xml',
                'security/ir.model.access.csv',

             'views/patient.xml',
             'views/doctor.xml',
             'views/department.xml',
             'views/customer.xml',
             
                 'reports/patient_template.xml',
                 'reports/reports.xml'
    ]
    
}