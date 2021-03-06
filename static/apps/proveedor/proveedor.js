$(document).ready(function () {
    var option = $('input[name="option"]').val();
    if (option === 'editar') {
        $('#id_numero_documento').attr('readonly', 'true');
        $('#id_documento').attr('readonly', 'true');
        $('select[readonly="readonly"] option:not(:selected)').attr('disabled', true);

    }

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-z," "]+$/i.test(value);
    }, "Letters and spaces only please");


    $.validator.setDefaults({
        errorClass: 'form-txt-danger',

        highlight: function (element, errorClass, validClass) {
            $(element)

                .addClass("form-control-danger")
                .removeClass("form-control-success");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element)

                .addClass("form-control-success")
                .removeClass("form-control-danger");
        }
    });
    $("#form").validate({
        rules: {
            nombres: {
                required: true,
                minlength: 10,
                maxlength: 50,
                lettersonly: true,
            },
            documento: {
                required: true
            },
            numero_documento: {
                required: true,
                minlength: 10,
                maxlength: 13,
                digits: true
            },
            correo: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
                minlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },


        },
        messages: {
            nombres: {
                required: "Porfavor ingresa tus nombres y apellidos",
                minlength: "Debe ingresar al menos un nombre y un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            numero_documento: {
                required: "Porfavor ingresa tu numero de documento",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 13 digitos",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Porfavor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Porfavor ingresa una direccion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_nombres').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });

});
