# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class StudentModel(models.Model):
    _name = 'curso.alumno'
    _description = 'Alumno'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('res.partner', string='Estudiante')

    student_phone = fields.Char(related='name.mobile', string='Teléfono', store=True)
    student_email = fields.Char(related='name.email', string='Correo', store=True)
    student_address = fields.Char(related='name.street', string='Dirección', store=True)
    student_dni = fields.Char(related='name.vat', string='DNI', store=True)
    student_state = fields.Char(related='name.state_id.name', string='Departamento', store=True)
    student_social_net = fields.Many2one('curso.medio' ,string='¿Cómo te enteraste del curso?', store=True)

    estado = fields.Selection([('creado','Creado'),('pedido','Con pedido'),('comprobado','Comprobado'),('enviado','Enviado')], string='Estado', tracking=True)

    usuario = fields.Char('Usuario', tracking=True)
    password = fields.Char('Contraseña', tracking=True)
    
    show_password = fields.Boolean('Activar', tracking=True)

    student_cod_certificado = fields.Char('Código de certificado', tracking=True)
            
    curso_ids = fields.One2many('curso.inscripcion', 'alumno_id', string='Cursos Inscritos')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    
    factura_ids = fields.Many2many('account.move', string='Facturas', compute='_compute_factura_ids', inverse='_inverse_factura_ids')

    @api.depends('name.invoice_ids', 'name.invoice_ids.state')
    def _compute_factura_ids(self):
        for record in self:
            if record.name:
                facturas = self.env['account.move'].search([
                    ('partner_id', '=', record.name.id),
                    ('move_type', '=', 'out_invoice'),  # Solo facturas de cliente
                    ('state', '=', 'posted')  # Solo facturas confirmadas
                ])
                record.factura_ids = facturas
            else:
                record.factura_ids = False

    def _inverse_factura_ids(self):
        pass  # Este método se puede dejar vacío

class AccountMove(models.Model):
    _inherit = 'account.move'

    alumno_ids = fields.Many2many('curso.alumno', string='Alumnos', compute='_compute_alumno_ids', store=True)

    @api.depends('partner_id', 'state')
    def _compute_alumno_ids(self):
        for record in self:
            alumnos = self.env['curso.alumno'].search([('name', '=', record.partner_id.id)])
            record.alumno_ids = alumnos