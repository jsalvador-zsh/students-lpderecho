# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class InscripcionModel(models.Model):
    _name = 'curso.inscripcion'
    _description = 'Inscripción de Alumno en Curso'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    curso_id = fields.Many2one('curso.curso', string='Curso', required=True, tracking=True)
    alumno_id = fields.Many2one('curso.alumno', string='Alumno', required=True, tracking=True)

    correo = fields.Char(related='alumno_id.student_email', string='Correo')
    telefono = fields.Char(related='alumno_id.student_phone', string='Teléfono')

    usuario = fields.Char(related='alumno_id.usuario', string='Usuario')
    cod_certificado = fields.Char('Código de certificado', tracking=True)
    sequence = fields.Char(string='N° de orden', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
        
    estado = fields.Selection([('creado','Creado'),('pedido','Con pedido'),('comprobado','Comprobado'),('enviado','Enviado')], string='Estado', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('inscripcion') or 'New'
        result = super(InscripcionModel, self).create(vals)
        return result

    # Nuevos campos
    num_examenes = fields.Integer(related= 'curso_id.num_examenes', string='Número de exámenes', tracking=True)

    examen_1 = fields.Float(string='Examen 1', tracking=True)
    examen_2 = fields.Float(string='Examen 2', tracking=True)
    examen_3 = fields.Float(string='Examen 3', tracking=True)
    promedio_examenes = fields.Float(string='Promedio de exámenes', compute='_compute_promedio_examenes')
    # Campo para definir el número de sesiones habilitadas
    num_sesiones = fields.Integer(related= 'curso_id.num_sesiones', string='Número de sesiones', tracking=True)

    # Campos de sesión
    sesion_1 = fields.Boolean(string='Sesión 1', tracking=True)
    sesion_2 = fields.Boolean(string='Sesión 2', tracking=True)
    sesion_3 = fields.Boolean(string='Sesión 3', tracking=True)
    sesion_4 = fields.Boolean(string='Sesión 4', tracking=True)
    sesion_5 = fields.Boolean(string='Sesión 5', tracking=True)
    sesion_6 = fields.Boolean(string='Sesión 6', tracking=True)
    sesion_7 = fields.Boolean(string='Sesión 7', tracking=True)
    sesion_8 = fields.Boolean(string='Sesión 8', tracking=True)

    numero_asistencias = fields.Integer(string='Número de asistencias', compute='_compute_numero_asistencias', store=True, tracking=True)
    puntos_por_asistencia = fields.Integer(string='Puntos por asistencia', compute='_compute_puntos_por_asistencia', store=True, tracking=True)
    promedio_final = fields.Float(string='Promedio final', compute='_compute_promedio_final', store=True, tracking=True)
    nota_certificado = fields.Float(string='Nota de certificado', tracking=True)
    envio_notas_finales = fields.Boolean(string='Envío de notas finales', tracking=True)
    confirmo_nombres_apellidos = fields.Boolean(string='Confirmó nombres', tracking=True)
    foto_certificado = fields.Boolean(string='Foto certificado', tracking=True)
    
    notificacion_examen_1 = fields.Boolean(string='Notificación de examen 1', tracking=True)
    notificacion_examen_2 = fields.Boolean(string='Notificación de examen 2', tracking=True)
    notificacion_examen_3 = fields.Boolean(string='Notificación de examen 3', tracking=True)


    #Datos quee varían por curso
    tarifa_id = fields.Many2one('curso.tarifa', string='Tarifa de inscripción')
    modalidad = fields.Selection([('1', 'Presencial'),('2','Virtual')], string='Modalidad')

    producto = fields.Many2many('product.product', string='Producto adicional')
    confirmacion = fields.Many2one('sending.type', string='Confirmación')
    material_escritorio = fields.Boolean('Material de escritorio', default = True)

    #Multiempresa
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

    @api.depends('sesion_1', 'sesion_2', 'sesion_3', 'sesion_4')
    def _compute_numero_asistencias(self):
        for student in self:
            student.numero_asistencias = sum([student.sesion_1, student.sesion_2, student.sesion_3, student.sesion_4])

    @api.depends('numero_asistencias')
    def _compute_puntos_por_asistencia(self):
        for student in self:
            if student.numero_asistencias >= 4:
                student.puntos_por_asistencia = 2
            elif 2 <= student.numero_asistencias <= 3:
                student.puntos_por_asistencia = 1
            else:
                student.puntos_por_asistencia = 0

    @api.depends('examen_1','examen_2','examen_3')
    def _compute_promedio_examenes(self):
        for student in self:
            notas = [student.examen_1, student.examen_2, student.examen_3]
            notas_presentes = [nota for nota in notas if nota > 0]

            if notas_presentes:
                student.promedio_examenes = sum(notas_presentes) / len(notas_presentes)
            else:
                student.promedio_examenes = 0

    @api.depends('promedio_examenes', 'puntos_por_asistencia')
    def _compute_promedio_final(self):
        for student in self:
            student.promedio_final = student.promedio_examenes + student.puntos_por_asistencia

    @api.onchange('promedio_final')
    def _onchange_promedio_final(self):
        for student in self:
            student.nota_certificado = student.promedio_final
