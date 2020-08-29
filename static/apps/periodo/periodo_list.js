$(function () {

    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        createdRow: function (row, data, dataIndex) {
            if (data[4] === '<span>ACTIVO</span>') {
                $('td', row).eq(4).find('span').addClass('badge badge-pill badge-success');
                $('td', row).eq(5).find('a[rel="estado"]').hide();
            } else if (data[4] === '<span>INACTIVO</span>') {
                $('td', row).eq(4).find('span').addClass('badge badge-pill badge-danger');
            }

        }

    });

    $('#datatable tbody').on('click', 'a[rel="estado"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/periodo/estado', 'Esta seguro que desea hacer a este periodo el actual?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito en la actualizacion', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });


});