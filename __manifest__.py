# -*- coding: utf-8 -*-
{
    "name": "HR & Recruitment Portal",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "summary": "Manage recruitment processes and employee portal.",
    "description": """
        This module extends HR features to provide a full recruitment workflow
        from the website and an internal portal for employees.
    """,
    "author": "Lan Anh",
    "category": "Human Resources",
    "depends": [
        "base",
        "hr",
        "hr_recruitment",
        "website",
    ],
    "data": [
        # Security first
        "security/ir.model.access.csv",
        # Then views
        "views/hr_employee_view.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
