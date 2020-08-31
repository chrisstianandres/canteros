$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data[5] >= 51) {
                $('td', row).eq(5).find('span').addClass('badge badge-pill badge-success');
            } else if (data[5] >= 10) {
                $('td', row).eq(5).find('span').addClass('badge badge-pill badge-warning');
            } else if (data[5] <= 9) {
                $('td', row).eq(5).find('span').addClass('badge badge-pill badge-danger');
            }

        }

    });
        $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/producto/eliminar', 'Esta seguro que desea eliminar este producto?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el producto!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});