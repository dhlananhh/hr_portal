from odoo import http
from odoo.http import request


class HrPortalController(http.Controller):

    @http.route("/jobs", type="http", auth="public", website=True)
    def jobs_list(self, **kwargs):
        jobs = request.env["hr.job"].sudo().search([("website_published", "=", True)])
        return request.render("om_hr_portal.jobs_page", {"jobs": jobs})

    @http.route(
        "/jobs/apply/submit", type="http", auth="public", website=True, methods=["POST"]
    )
    def apply_for_job_submit(self, **kwargs):
        job_id = int(kwargs.get("job_id", 0))

        applicant = (
            request.env["hr.applicant"]
            .sudo()
            .create(
                {
                    "name": f"{kwargs.get('partner_name')}'s Application",
                    "partner_name": kwargs.get("partner_name"),
                    "email_from": kwargs.get("email_from"),
                    "partner_phone": kwargs.get("partner_phone"),
                    "job_id": job_id,
                    "department_id": request.env["hr.job"]
                    .browse(job_id)
                    .department_id.id,
                }
            )
        )

        if "ufile" in request.params:
            attachment = (
                request.env["ir.attachment"]
                .sudo()
                .create(
                    {
                        "name": kwargs.get("ufile").filename,
                        "res_name": applicant.name,
                        "res_model": "hr.applicant",
                        "res_id": applicant.id,
                        "datas": request.params["ufile"].read(),
                        "mimetype": kwargs.get("ufile").content_type,
                    }
                )
            )
            applicant.attachment_ids = [(4, attachment.id)]

        return request.render("om_hr_portal.apply_form_success")

    @http.route("/my/profile", type="http", auth="user", website=True)
    def my_profile(self, **kwargs):
        employee = request.env.user.employee_id

        if not employee:
            return request.render("om_hr_portal.portal_not_an_employee")

        values = {"employee": employee}
        return request.render("om_hr_portal.portal_my_profile", values)
