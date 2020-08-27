$(function () {
    $('#save').on('click', function () {
        if ($('input[name="username"]').val() === "") {
            menssaje_error('Error!', "Debe ingresar un Username", 'far fa-times-circle');
            return false
        } else if ($('input[name="password"]').val() === "") {
            menssaje_error('Error!', "Debe ingresar una contraseña", 'far fa-times-circle');
            return false
        }
        var parametros;
        parametros = {
            'username': $('input[name="username"]').val(),
            'password': $('input[name="password"]').val()
        };
        login('/connect/', parametros, function () {
                 window.$.dialog({
                    icon: 'fa fa-spinner fa-spin',
                    title: 'Iniciando Sesion!',
                    content: false
                });
                setTimeout(function () {
                    location.href = '/';
                }, 2000);

            });
    });
});

