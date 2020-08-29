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
        order: [[ 3, "desc" ]],
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',

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
            if (data[4] === '<span>FINALIZADA</span>') {
                $('td', row).eq(4).find('span').addClass('badge badge-pill badge-success');
                $('td', row).eq(5).find('a[rel="estado"]').hide();
                $('td', row).eq(5).find('a[rel="edit"]').hide();
            } else if (data[4] === '<span>PENDIENTE</span>') {
                $('td', row).eq(4).find('span').addClass('badge badge-pill badge-warning');
            }

        }
    });

    $('#datatable tbody').on('click', 'a[rel="estado"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['3']};
        save_estado('Alerta',
            '/compra/estado', 'Esta seguro que desea finalizar esta compra?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al finalizar la compra', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });

    }).on('click', 'a[rel="borrar"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['3']};
        save_estado('Alerta',
            '/compra/eliminar', 'Esta seguro que desea eliminar esta compra?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al Eliminar la compra', 'far fa-smile-wink')
            });

    })
        .on('click', 'a[rel="detalle"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        $('#Modal').modal('show');
        $("#tbldetalle_insumos").DataTable({
            responsive: true,
            autoWidth: false,
            language: {
                "url": '../static/lib/datatables-1.10.20/spanish.txt'
            },
            destroy: true,
            ajax: {
                url: '/asig_insumo/get_detalle',
                type: 'Post',
                data: {
                    'id': data['0']
                },
                dataSrc: ""
            },
            columns: [
                {data: 'insumo.nombre'},
                {data: 'insumo.categoria.nombre'},
                {data: 'insumo.presentacion.nombre'},
                {data: 'cantidad'}
            ],
            columnDefs: [
                {
                    targets: [3],
                    class: 'text-center'
                }
            ],
        });

    });

});

function pad (str, max) {
  str = str.toString();
  return str.length < max ? pad("0" + str, max) : str;
}
