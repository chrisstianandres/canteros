$(document).ready(function () {

    $('input[name="valor_dim"]').TouchSpin({
        min: 1,
        max: 1000000,
        forcestepdivisibility: 'none',
        boostat: 5,
        maxboostedstep: 10
    });


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
        },
        messages: {
            nombre: {
                required: "Porfavor ingresa el nombre del cantero",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
        },
    });

    $('#id_nombre').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0,1).toUpperCase()+pal.substr(1);
        $(this).val(changue);
    });

});
