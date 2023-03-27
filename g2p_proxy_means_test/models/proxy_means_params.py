# Part of OpenG2P Registry. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class G2PProgram(models.Model):
    _inherit = "g2p.program"

    pmt_config = fields.Boolean(string="Opt for PMT Config")
    proxy_means_params_id = fields.One2many("g2p.proxy_means_test_params", "program_id", string="PMT Parameters")
    
class ProxyMeanTestParams(models.Model):

    _name = "g2p.proxy_means_test_params"
    _description = "Proxy Means Test Params"

    program_id = fields.Many2one("g2p.program", default= lambda self: self.env.uid)
    pmt_field = fields.Many2one("g2p.program_membership", string="Field")
    pmt_weightage = fields.Float(string="Weightage")  

        
class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    pmt_score = fields.Integer(
        "PMT Score", compute="_compute_pmt_score", store=True
    )

    def name_get(self):
        result = []
        for rec in self:
            for name in rec.fields_get_keys():
                result.append((rec.id, name))

        return result

    @api.depends("program_id")
    def _compute_pmt_score(self):
        data = self.env["g2p.proxy_means_test_params"].search([("program_id", "=", self.program_id.id)])
        score = 0
        for rec in data:
            score += rec.pmt_weightage

        self.pmt_score = score

