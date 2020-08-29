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
        columnDefs: [
            {
                targets: -1,
                class: 'text-center',

            },
        ],
    });

    $('#datatable tbody').on('click', 'a[rel="detalle"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        $('#Modal').modal('show');
        $("#tbldetalle_asig").DataTable({
            responsive: true,
            autoWidth: false,
            language: {
                "url": '../static/lib/datatables-1.10.20/spanish.txt'
            },
            destroy: true,
            ajax: {
                url: '/produccion/get_detalle',
                type: 'Post',
                data: {
                    'id': data['0']
                },
                dataSrc: ""
            },
            columns: [
                {data: 'fecha'},
                {data: 'periodo.nombre'},
                {data: 'producto.nombre'},
                {data: 'producto.presentacion.nombre'},
                {data: 'cantidad'}

            ],
            order: [[0, "desc"]],
        });

    });

});

