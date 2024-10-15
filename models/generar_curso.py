from odoo import models, fields, _, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_create_curso(self):
        try:
            # Buscar el producto por su nombre
            product = self.env['product.product'].search([('name', '=', self.name)], limit=1)
            
            if not product:
                raise ValueError(_('No se encontró el producto con el nombre proporcionado.'))

            # Crear un registro en curso.curso usando el ID del producto encontrado
            self.env['curso.curso'].create({
                'name': product.id,  # Usar el ID del producto encontrado
                'materia_id': self.categ_id.id,  # Tomamos el categ_id del producto para materia_id
            })

            # Retornar la acción para mostrar la notificación de éxito
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'title': _('Registro registrado'),
                    'message': _('El curso fue creado correctamente.'),
                    'sticky': False,
                }
            }

        except Exception as e:
            # En caso de error, mostrar una notificación de error
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'danger',
                    'title': _('Error al registrar'),
                    'message': _('No se pudo crear el curso. Error: %s' % str(e)),
                    'sticky': False,
                }
            }
