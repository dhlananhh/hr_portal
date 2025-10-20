# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class JobPortal(http.Controller):

    @http.route("/jobs", type="http", auth="public", website=True)
    def jobs_list(self, **kwargs):
        """
        This controller fetches all published jobs and renders the jobs listing page.
        """
        published_jobs = (
            request.env["hr.job"]
            .sudo()
            .search(
                [
                    ("is_published", "=", True),
                    ("website_id", "in", (False, request.website.id)),
                ]
            )
        )

        return request.render(
            "om_hr_portal.job_list_template", {"jobs": published_jobs}
        )

    @http.route(
        '/jobs/detail/<model("hr.job"):job>', type="http", auth="public", website=True
    )
    def job_detail(self, job, **kwargs):
        """
        This controller renders the detail page for a specific job.
        It also creates a new applicant if the form is submitted.
        """
        return request.render("om_hr_portal.job_detail_template", {"job": job})

    @http.route(
        "/jobs/apply", type="http", auth="public", website=True, methods=["POST"]
    )
    def job_apply(self, **post):
        """
        Controller to handle the job application form submission.
        """
        # Create a new applicant record
        applicant = (
            request.env["hr.applicant"]
            .sudo()
            .create(
                {
                    "name": f"{post.get('applicant_name')}'s Application",
                    "partner_name": post.get("applicant_name"),
                    "email_from": post.get("applicant_email"),
                    "partner_phone": post.get("applicant_phone"),
                    "job_id": int(post.get("job_id")),
                }
            )
        )

        # Attach the CV if one was uploaded
        if "cv_file" in request.params:
            attachment = (
                request.env["ir.attachment"]
                .sudo()
                .create(
                    {
                        "name": request.params.get("cv_file").filename,
                        "res_name": applicant.name,
                        "res_model": "hr.applicant",
                        "res_id": applicant.id,
                        "datas": http.pycompat.to_text(
                            request.params.get("cv_file").read()
                        ),
                    }
                )
            )
            applicant.attachment_ids = [(4, attachment.id)]

        # Redirect to a thank you page
        return request.render("om_hr_portal.job_thank_you_template")
