$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        createdRow: function (row, data, dataIndex) {
            if (data[4] === 'ACTIVO') {
                $('td', row).eq(3).addClass('badge badge-primary');
            } else if (data[4] === 'INACTIVO') {
                $('td', row).eq(3).addClass('badge badge-danger');
            }

        }

    });

    $('#datatable tbody').on('click', 'a[rel="estado"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/cantero/estado', 'Esta seguro que desea cambiar el estado de este cantero?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito en la actualizacion', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});

