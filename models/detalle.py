# -*- coding: utf-8 -*-
from odoo import fields, models

class DetalleCursoModel(models.Model):
    _name = 'curso.detalle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Detalle', required = True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

class TarifaInscripcion(models.Model):
    _name = 'curso.tarifa'
    _description = 'Tarifa de Inscripción'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tarifa', required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

class ConvenioModel(models.Model):
    _name = 'curso.convenio'
    _description = 'Convenio'

    name = fields.Char('Nombre', required=True)
    entidad = fields.Many2one('res.partner', string='Entidad')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

class MedioSociallModel(models.Model):
    _name = 'curso.medio'
    _description = 'Medio por el cual se enteró del curso'

    name = fields.Char(string='Medio / Red social', required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
