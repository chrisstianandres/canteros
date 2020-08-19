var datatable;
$(function () {

    datatable = $("#datatable").DataTable({
        // responsive: true,
        destroy: true,
        scrollX: true,
        autoWidth: false,
        language: {
            "url": '../static/lib/datatables-1.10.20/spanish.txt'
        },
        order: [[ 5, "desc" ]],
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',

            },
            {
                    targets: [2, 3, 4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            {
                targets: [-1],
                class: 'text-center',
                width: "10%",
            },
            {
                targets: [-3],
                render: function (data, type, row) {
                        return pad(data, 10);
                    }
            }
        ],
        createdRow: function (row, data, dataIndex) {
            if (data[6] === '<span>FINALIZADA</span>') {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-success');
                $('td', row).eq(7).find('a[rel="estado"]').hide();
                $('td', row).eq(7).find('a[rel="edit"]').hide();
            } else if (data[6] === '<span>PENDIENTE</span>') {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-warning');
            }

        }
    });

    $('#datatable tbody').on('click', 'a[rel="estado"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['5']};
        save_estado('Alerta',
            '/venta/estado', 'Esta seguro que desea finalizar esta venta?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al finalizar la venta', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });

    }).on('click', 'a[rel="borrar"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['5']};
        save_estado('Alerta',
            '/venta/eliminar', 'Esta seguro que desea eliminar esta venta?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al Eliminar la venta', 'far fa-smile-wink')
            });
    }).on('click', 'a[rel="detalle"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        $('#Modal').modal('show');
        $("#tbldetalle_productos").DataTable({
            responsive: true,
            autoWidth: false,
            language: {
                "url": '../static/lib/datatables-1.10.20/spanish.txt'
            },
            destroy: true,
            ajax: {
                url: '/venta/get_detalle',
                type: 'Post',
                data: {
                    'id': data['5']
                },
                dataSrc: ""
            },
            columns: [
                {data: 'producto.nombre'},
                {data: 'producto.categoria.nombre'},
                {data: 'producto.presentacion.nombre'},
                {data: 'cantidad'},
                {data: 'producto.pvp'},
                {data: 'venta.subtotal'}
            ],
            columnDefs: [
                {
                    targets: [5],
                    class: 'text-center'
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
        });

    });

});

function pad (str, max) {
  str = str.toString();
  return str.length < max ? pad("0" + str, max) : str;
}
