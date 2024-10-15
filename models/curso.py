# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import date, timedelta
import dateutil.relativedelta

class CursoModel(models.Model):
    _name = 'curso.curso'
    _description = 'Curso'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('product.product',string='Nombre', required = True)

    enlace_aula = fields.Char('Link del aula', tracking=True)
    enlace_db = fields.Char('Link de la BD', tracking=True)
    num_sesiones = fields.Integer(string='Número de Sesiones', tracking=True)
    num_examenes = fields.Integer(string='Número de Exámenes', tracking=True)
    fecha_inicio = fields.Date('Fecha inicio', tracking=True)
    fecha_fin = fields.Date('Fecha fin', tracking=True)
    vigencia = fields.Char('Vigencia', tracking=True)
    cancelar = fields.Date('Cancelar', compute='_compute_cancelar', store=True)
    estado_aula = fields.Selection([('habilitado','Habilitado'),('cancelando','Cancelando'),('cancelado','Cancelado')], string = 'Estado aula')
    
    estado_curso = fields.Selection([('culmino','Culminó'),('vigente','Vigente')], string = 'Estado', compute='_compute_estado_curso', store=True)
    nota = fields.Char('Nota', tracking=True)

    detalle_id  = fields.Many2one('curso.detalle', string='Detalle')
    materia_id  = fields.Many2one('product.category', string='Materia')
    tipo_capacitacion = fields.Selection([('regular','Regular'),('gratuito','Gratuito'),('corto','Corto')], string = 'Tipo de capacitación', tracking=True)
    cancelado = fields.Many2one('res.users', string = 'Cancelado por')
    convenio = fields.Many2many('curso.convenio', string='Convenios', tracking=True)
    certificado = fields.Selection([('digpar','Digital - Participación'),('digapro','Digital - Aprobación'),('fispar','Físico - Participación'),('fisapro','Físico - Aprobación')], string = 'Certificación', tracking=True)
    estado_certificado = fields.Selection([('plazo','En plazo'),('tramite','En trámite'),('entrega','Entrega')], string = 'Estado certificación', tracking=True)
    detalle_curso = fields.Text('Detalle', tracking=True)
    #Multiempresa
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

    students_ids = fields.Many2many('curso.alumno', string='Alumnos')

    # Nuevos campos de confirmación
    confirmar_envio_notas_finales = fields.Boolean(string='Confirmar Envío Notas Finales', tracking=True)
    confirmar_nombres_apellidos = fields.Boolean(string='Confirmar Nombres y Apellidos', tracking=True)
    confirmar_foto_certificado = fields.Boolean(string='Confirmar Foto Certificado', tracking=True)

    def action_confirmar_envio_notas_finales(self):
        self.confirmar_envio_notas_finales = True
        inscripciones = self.env['curso.inscripcion'].search([('curso_id', '=', self.id)])
        inscripciones.write({'envio_notas_finales': True})

    def action_confirmar_nombres_apellidos(self):
        self.confirmar_nombres_apellidos = True
        inscripciones = self.env['curso.inscripcion'].search([('curso_id', '=', self.id)])
        inscripciones.write({'confirmo_nombres_apellidos': True})

    def action_confirmar_foto_certificado(self):
        self.confirmar_foto_certificado = True
        inscripciones = self.env['curso.inscripcion'].search([('curso_id', '=', self.id)])
        inscripciones.write({'foto_certificado': True})

    @api.depends('fecha_fin', 'vigencia')
    def _compute_cancelar(self):
        for record in self:
            if record.fecha_fin and record.vigencia:
                try:
                    vigencia_meses = int(record.vigencia)
                    nueva_fecha = record.fecha_fin + dateutil.relativedelta.relativedelta(months=vigencia_meses)
                    record.cancelar = nueva_fecha + timedelta(days=2)
                except ValueError:
                    record.cancelar = False
            else:
                record.cancelar = False

    @api.depends('fecha_fin')
    def _compute_estado_curso(self):
        for record in self:
            if record.fecha_fin:
                if record.fecha_fin < date.today():
                    record.estado_curso = 'culmino'
                else:
                    record.estado_curso = 'vigente'
            else:
                record.estado_curso = False

    # Método para abrir la vista de inscripciones
    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Estudiantes Inscritos'),
            'view_mode': 'tree,form',
            'res_model': 'curso.inscripcion',
            'domain': [('curso_id', '=', self.id)],
            'context': {'default_curso_id': self.id},
        }