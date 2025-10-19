{
    "name": "HR & Recruitment Portal",
    "version": "18.0.1.0.0",
    "summary": "Manage recruitment processes and employee portal.",
    "description": """
        This module extends HR features to provide a full recruitment workflow
        from the website and an internal portal for employees.
    """,
    "author": "Lan Anh",
    "category": "Human Resources",
    "license": "LGPL-3",
    "depends": [
        "hr",
        "hr_recruitment",
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_view.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
