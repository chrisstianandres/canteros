$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
        },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a rel="edit" href="/labor/editar/' + data + '" type="button" class="btn btn-primary btn-sm btn-flat btn-round" style="color: white" data-toggle="tooltip" title="Editar Insumo"><i class="fa fa-edit"></i></a>' + ' ';
                    var del = '<a rel="del" type="button" class="btn btn-danger btn-sm btn-flat btn-round" style="color: white" data-toggle="tooltip" title="Eliminar Labor"><i class="fa fa-trash-alt"></i></a>';
                    return edit + del;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data[5] <= 0) {
                $('td', row).eq(5).find('span').addClass('badge badge-pill badge-danger');
            } else if (data[5] < 50) {
                $('td', row).eq(5).find('span').addClass('badge badge-pill badge-warning');
            } else if (data[5] >= 21) {
                $('td', row).eq(5).find('span').addClass('badge badge-pill badge-success');
            }

        }

    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/labor/eliminar', 'Esta seguro que desea eliminar esta labor?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar la labor!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});
