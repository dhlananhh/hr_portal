# -*- coding: utf-8 -*-
import base64
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


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
        try:
            # 1. Create the candidate record first. This model holds the person's info.
            candidate = (
                request.env["hr.candidate"]
                .sudo()
                .create(
                    {
                        "name": post.get("applicant_name"),
                        "email_from": post.get("applicant_email"),
                        "partner_phone": post.get("applicant_phone"),
                    }
                )
            )

            # 2. Create the applicant record, linking it to the newly created candidate.
            applicant = (
                request.env["hr.applicant"]
                .sudo()
                .create(
                    {
                        "partner_name": post.get("applicant_name"),
                        "email_from": post.get("applicant_email"),
                        "partner_phone": post.get("applicant_phone"),
                        "job_id": int(post.get("job_id")),
                        "candidate_id": candidate.id,
                    }
                )
            )

            # Attach the CV if one was uploaded
            if "cv_file" in request.params:
                attachment_data = request.params.get("cv_file").read()
                request.env["ir.attachment"].sudo().create(
                    {
                        "name": request.params.get("cv_file").filename,
                        "res_model": "hr.applicant",
                        "res_id": applicant.id,
                        "datas": base64.b64encode(attachment_data),
                    }
                )

            # Redirect to the thank you page
            return request.render("om_hr_portal.job_thank_you_template")

        except Exception as e:
            # In case of any error, render a clean error page.
            # We log the error to the terminal for debugging purposes.
            _logger.error(f"Error during job application submission: {e}")
            return request.render("om_hr_portal.job_error_template", {"error": e})
