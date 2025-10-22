# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJob(models.Model):
    _inherit = "hr.job"

    job_type = fields.Selection(
        [
            ("full_time", "Full-time"),
            ("part_time", "Part-time"),
            ("contract", "Contract"),
            ("internship", "Internship"),
        ],
        string="Job Type",
        default="full_time",
    )
