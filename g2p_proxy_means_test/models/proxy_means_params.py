# Part of OpenG2P Registry. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from lxml import etree

class G2PProgram(models.Model):
    _inherit = "g2p.program"

    pmt_config = fields.Boolean(string="Opt for PMT Config")
    proxy_means_params_id = fields.One2many("g2p.proxy_means_test_params", "program_id", string="PMT Parameters")
    
class ProxyMeanTestParams(models.Model):

    _name = "g2p.proxy_means_test_params"
    _description = "Proxy Means Test Params"

    program_id = fields.Many2one("g2p.program")
    pmt_field = fields.Many2one("g2p.program_membership", string="Field")
    pmt_weightage = fields.Float(string="Weightage")  

    # def _get_program_id(self):
    #     print("-----------------test----------")
    #     print(self)

    # def add_new_field(self):
    #     view_id = self.env.ref('g2p_proxy_means_test.view_config_proxy_means_test_form').id
    #     view = self.env['ir.ui.view'].browse(view_id)
    #     view_arch = etree.fromstring(view.arch)
    #     new_field = etree.Element('field', {'name': 'pmt_field'})
    #     view_arch.xpath("//group")[0].append(new_field)
    #     view.write({'arch': etree.tostring(view_arch)})
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'g2p.proxy_means_test_params',
    #         'res_id': self.id,
    #         'view_mode': 'form',
    #         'view_id': view_id,
    #         'target': 'current',
    #     }
        
class G2PProgramMembership(models.Model):
    _inherit = "g2p.program_membership"

    pmt_score = fields.Integer(
        "PMT Score", compute="_compute_pmt_score", store=True
    )

    # def name_get(self):
    #     result = []
    #     for rec in self.fields_get_keys():
    #         if rec[0] == 'x':
    #             result.append((rec, rec))
    #     return result

    @api.depends("program_id")
    def _compute_pmt_score(self):
        data = self.env["g2p.proxy_means_test_params"].search([("program_id", "=", self.program_id.id)])
        score = 0
        for rec in data:
            score += rec.pmt_weightage

        self.pmt_score = score

