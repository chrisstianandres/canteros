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
                targets: [0, -1],
                class: 'text-center',
                width: "8%",
            }
        ],
    });

    $('#datatable tbody').on('click', 'a[rel="detalle"]', function () {
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
