$(document).ready(function () {

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
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            desde_day: {
                required: true
            },
            desde_month: {
                required: true
            },
            desde_year: {
                required: true
            },
           hasta_day: {
                required: true
            },
            hasta_month: {
                required: true
            },
            hasta_year: {
                required: true
            },
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre de la categoria",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            } ,
            desde_day: {
                required: "Por favor escoge una dia"

            } ,
            desde_month: {
                required: "Por favor escoge un mes"

            } ,
            desde_year: {
                required: "Por favor escoge un año"

            } ,
            hasta_day: {
                required: "Por favor escoge una fecha"
            },
            hasta_month: {
                required: "Por favor escoge una mes"
            },
            hasta_year: {
                required: "Por favor escoge una año"
            },
        },
    });

    $('#id_nombre').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
});
