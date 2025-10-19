from odoo import http
from odoo.http import request


class HrRecruitmentController(http.Controller):

    @http.route("/jobs", type="http", auth="public", website=True)
    def jobs_list(self, **kwargs):
        jobs = request.env["hr.job"].sudo().search([("website_published", "=", True)])

        return request.render("om_hr_portal.jobs_page", {"jobs": jobs})
