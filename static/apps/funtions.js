function borrar_todo_alert(title, content, callback, callback2) {
    $.confirm({
        title: title,
        icon: 'fas fa-exclamation-triangle',
        type: 'red',
        typeAnimated: true,
        content: content,
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    callback();
                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red'
            },
        }
    });
}

function save_with_ajax(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        menssaje_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                    //

                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {

                }
            }
        }
    });
}

function save_estado(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        menssaje_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {
                    });
                    //

                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {
                }
            }
        }
    });
}

function menssaje_error(title, content, icon) {
    $.confirm({
        theme: 'modern',
        icon: icon,
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue',
            },
        }
    });
}

function menssaje_ok(title, content, icon, callback) {
    $.confirm({
        theme: 'modern',
        icon: icon,
        type:'green',
        title: title,
        content: content,
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue',
                action: function () {
                   callback();
                }
            },
        }
    });
}

