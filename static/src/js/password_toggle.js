odoo.define('students.password_toggle', function (require) {
    "use strict";
    
    var FormRenderer = require('web.FormRenderer');
    
    FormRenderer.include({
        _renderFieldWidget: function (node) {
            this._super.apply(this, arguments);

            if (node.attrs.name === "show_password") {
                var $passwordField = this.$el.find('input[name="password"]');
                var $toggleField = this.$el.find('input[name="show_password"]');

                $toggleField.on('change', function () {
                    if ($toggleField.prop('checked')) {
                        $passwordField.prop('type', 'text');  // Muestra la contraseña
                    } else {
                        $passwordField.prop('type', 'password');  // Oculta la contraseña
                    }
                });
            }
        }
    });
});
