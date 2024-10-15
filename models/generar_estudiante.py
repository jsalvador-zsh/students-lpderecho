from odoo import fields, models, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_create_student_and_enrollment(self):
        for move in self:
            # Verifica si el alumno ya existe
            student = self.env['curso.alumno'].search([('name', '=', move.partner_id.id)], limit=1)
            if not student:
                # Crea un nuevo alumno
                student = self.env['curso.alumno'].create({
                    'name': move.partner_id.id,
                    'usuario': move.partner_id.email,  # Asumiendo que el email será el usuario
                    'password': 'default_password',  # Puedes personalizar la lógica de generación de contraseña
                })

            # Obtiene los productos de tipo servicio de la línea de factura
            curso_productos = move.invoice_line_ids.filtered(lambda line: line.product_id.detailed_type == 'service').mapped('product_id')

            if not curso_productos:
                # Mostrar una notificación de que no hay un curso en la factura
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'warning',
                        'title': _('Curso no encontrado'),
                        'message': _('No se encontró un curso en las líneas de la factura.'),
                        'sticky': False,
                    }
                }

            for producto in curso_productos:
                # Buscar el curso en base al producto de la factura
                curso = self.env['curso.curso'].search([('name', '=', producto.id)], limit=1)

                if not curso:
                    # Mostrar una notificación de que el curso no está registrado
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'warning',
                            'title': _('Curso no registrado'),
                            'message': _('El curso no está registrado en el sistema.'),
                            'sticky': False,
                        }
                    }

                # Verifica si el alumno ya está matriculado en el curso
                existing_enrollment = self.env['curso.inscripcion'].search([
                    ('alumno_id', '=', student.id),
                    ('curso_id', '=', curso.id)
                ], limit=1)

                if existing_enrollment:
                    # Mostrar una notificación de que el alumno ya está matriculado en el curso
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'warning',
                            'title': _('Alumno matriculado'),
                            'message': _('El alumno ya está matriculado en este curso.'),
                            'sticky': False,
                        }
                    }

                # Crea una inscripción para el alumno y el curso
                self.env['curso.inscripcion'].create({
                    'alumno_id': student.id,
                    'curso_id': curso.id,
                    'modalidad': move.modalidad
                })

            # Mostrar una notificación de éxito al matricular al alumno
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'title': _('Alumno registrado y matriculado'),
                    'message': _('El alumno fue matriculado correctamente en todos los cursos.'),
                    'sticky': False,
                }
            }
