from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HREmployeeChangeRequest(models.Model):
    _name = "hr.employee.change.request"
    _description = "Employee Information Change Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        default=lambda self: self.env.user.employee_id,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="draft",
        track_visibility="onchange",
    )

    citizen_id = fields.Char(string="Citizen ID/CCCD")
    bank_account_number = fields.Char(string="Bank Account Number")
    personal_email = fields.Char(string="Personal Email")

    def action_submit(self):
        self.write({"state": "submitted"})

    def action_approve(self):
        if not self.env.user.has_group("hr.group_hr_manager"):
            raise UserError(_("Only HR Managers can approve requests."))

        vals_to_update = {}
        if self.citizen_id:
            vals_to_update["citizen_id"] = self.citizen_id
        if self.bank_account_number:
            vals_to_update["bank_account_number"] = self.bank_account_number
        if self.personal_email:
            vals_to_update["personal_email"] = self.personal_email

        if vals_to_update:
            self.employee_id.write(vals_to_update)

        self.write({"state": "approved"})
        self.message_post(
            body=_("Your information change request has been approved and updated.")
        )

    def action_reject(self):
        self.write({"state": "rejected"})
