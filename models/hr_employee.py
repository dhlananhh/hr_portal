# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    citizen_id = fields.Char(string="Citizen ID")
    bank_account_number = fields.Char(string="Bank Account Number")
    personal_email = fields.Char(string="Personal Email")
