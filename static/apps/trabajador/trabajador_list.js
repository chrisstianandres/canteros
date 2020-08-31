$(function () {
    var datatable = $("#datatable").DataTable({

        autoWidth: false,
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            }
        ],
        createdRow: function (row, data, dataIndex) {
            if (data[7] === 'ACTIVO') {
                $('td', row).eq(7).find('span').addClass('badge badge-primary');
            } else if (data[7] === 'INACTIVO') {
                $('td', row).eq(7).find('span').addClass('badge badge-danger');
            }

        }

    });

    $('#datatable tbody').on('click', 'a[rel="estado"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/trabajador/estado', 'Esta seguro que desea cambiar el estado de este trabajador?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito en la actualizacion', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});

