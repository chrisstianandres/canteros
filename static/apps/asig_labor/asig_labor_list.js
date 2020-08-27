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
                url: '/asig_labor/get_detalle',
                type: 'Post',
                data: {
                    'id': data['0']
                },
                dataSrc: ""
            },
            columns: [
                {data: 'fecha_asig'},
                {data: 'periodo.nombre'},
                {data: 'desde'},
                {data: 'hasta'},
                {data: 'labor.nombre'},
                {data: 'total_dias'},
                {data: 'valor_a_pag'},
                {data: 'saldo'},
                {data: 'valor_pag'},
                {data: 'estado'},
                {data: 'id'},

            ],
            order: [[ 9, "desc" ]],
            columnDefs: [
                {
                    targets: [3],
                    class: 'text-center'
                },
                {
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
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
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="pagar" href="/asig_labor/pago_jornada/'+data+'" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Pagar Jornada"><i class="fas fa-hand-holding-usd"></i></a>';
                    }
                },
            ],
             createdRow: function (row, data, dataIndex) {
            if (data.estado === 'PAGADO') {
                $('td', row).eq(9).find('span').addClass('badge badge-pill badge-success');
                $('td', row).eq(10).find('a[rel="pagar"]').hide();
            } else if (data.estado === 'PENDIENTE') {
                $('td', row).eq(9).find('span').addClass('badge badge-pill badge-warning');
            }

        }
        });

    });

});

