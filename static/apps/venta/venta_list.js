var datatable;
var logotipo;
const toDataURL = url => fetch(url).then(response => response.blob())
    .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob)
    }));

toDataURL('/media/canteros_logo.png').then(dataUrl => {
    logotipo = dataUrl;
});
var datos = {
    fechas: {
        'start_date': '',
        'end_date': ''
    },
    add: function (data) {
        if (data.key === 1) {
            this.fechas['start_date'] = data.startDate.format('YYYY-MM-DD');
            this.fechas['end_date'] = data.endDate.format('YYYY-MM-DD');
        } else {
            this.fechas['start_date'] = '';
            this.fechas['end_date'] = '';
        }

        $.ajax({
            url: '/venta/data',
            type: 'POST',
            data: this.fechas,
            success: function (data) {
                datatable.clear();
                datatable.rows.add(data).draw();
            }
        });

    },
};

function daterange() {
    $("div.toolbar").html('<br><div class="col-lg-3"><input type="text" name="fecha" class="form-control form-control-sm input-sm"></div> <br>');
    $('input[name="fecha"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-search"></i> Buscar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        picker['key'] = 1;
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        datos.add(picker);

    });

}

$(function () {
    datatable = $("#datatable").DataTable({
        // responsive: true,
        destroy: true,
        ajax: {
            url: '/venta/data',
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        dom: '<"top"B><"toolbar"><br>frtip',
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            searchPanes: {
                clearMessage: 'Limpiar Filtros',
                collapse: {
                    0: 'Filtros de Busqueda',
                    _: 'Filtros seleccionados (%d)'
                },
                title: {
                    _: 'Filtros seleccionados - %d',
                    0: 'Ningun Filtro seleccionados',
                },
                activeMessage: 'Filtros activos (%d)',
                emptyPanes: 'No existen suficientes datos para generar filtros :('

            }
        },
        buttons: [
            {
                text: '<i class="fa fa-search-minus"> Filtar por fecha</i>',
                className: 'btn btn-success btn-round my_class',
                action: function (e, dt, node, config) {
                    daterange();
                }
            },
            {
                className: 'btn btn-info btn-round my_class', extend: 'searchPanes',
                config: {
                    cascadePanes: true,
                    viewTotal: true,
                    layout: 'columns-4'
                }
            },
            {
                text: '<i class="fa fa-file-pdf"> Reporte PDF</i>',
                className: 'btn btn-danger btn-round my_class',
                extend: 'pdfHtml5',
                //filename: 'dt_custom_pdf',
                orientation: 'landscape', //portrait
                pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                download: 'open',
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6],
                    search: 'applied',
                    order: 'applied'
                },
                customize: function (doc) {
                    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                        "Septiembre", "Octubre", "Noviembre", "Diciembre"
                    ];

                    var date = new Date();

                    function formatDateToString(date) {
                        // 01, 02, 03, ... 29, 30, 31
                        var dd = (date.getDate() < 10 ? '0' : '') + date.getDate();
                        // 01, 02, 03, ... 10, 11, 12
                        // month < 10 ? '0' + month : '' + month; // ('' + month) for string result
                        var MM = monthNames[date.getMonth() + 1]; //monthNames[d.getMonth()])
                        // 1970, 1971, ... 2015, 2016, ...
                        var yyyy = date.getFullYear();
                        // create the format you want
                        return (dd + " de " + MM + " de " + yyyy);
                    }

                    var jsDate = formatDateToString(date);
                    //[izquierda, arriba, derecha, abajo]
                    doc.pageMargins = [20, 120, 25, 50];
                    doc.defaultStyle.fontSize = 10;
                    doc.styles.tableHeader.fontSize = 12;
                    doc['header'] = (function () {
                        return {
                            columns: [{alignment: 'center', image: logotipo, width: 300}],
                            margin: [280, 10, 0, 0] //[izquierda, arriba, derecha, abajo]
                        }
                    });
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Reporte creado el: ', {text: jsDate.toString()}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['Pagina ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });
                    var objLayout = {};
                    objLayout['hLineWidth'] = function (i) {
                        return .5;
                    };
                    objLayout['vLineWidth'] = function (i) {
                        return .5;
                    };
                    objLayout['hLineColor'] = function (i) {
                        return '#000000';
                    };
                    objLayout['vLineColor'] = function (i) {
                        return '#000000';
                    };
                    objLayout['paddingLeft'] = function (i) {
                        return 4;
                    };
                    objLayout['paddingRight'] = function (i) {
                        return 4;
                    };
                    doc.content[0].layout = objLayout;
                    doc.content[1].table.widths = [65, 95, 110, 60, 55, 120];
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
                }
            },
            {
                text: '<i class="fa fa-file-excel"> Reporte Excel</i>', className: "btn btn-success btn-round my_class",
                extend: 'excel'
            }
        ],
        order: [[5, "desc"]],
        columnDefs: [
             {
                searchPanes: {
                    show: true,
                },
                targets: [1,4, 5, 6],
            },
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
                render: function (data, type, row) {
                    var detalle = '<a type="button" rel="detalle" class="btn btn-success btn-sm btn-round" style="color: white" data-toggle="tooltip" title="Detalle de Productos"><i class="fa fa-search"></i></a>' + " ";
                    var devolver = '<a type="button" rel="devolver" class="btn btn-danger btn-sm btn-round" style="color: white" data-toggle="tooltip" title="Devolver"><i class="fa fa-times"></i></a>';
                    var pdf = '<a type="button" rel="pdf" class="btn btn-info btn-sm btn-round" style="color: white" data-toggle="tooltip" title="Comprobante"><i class="fa fa-file-pdf"></i></a>';
                    return detalle + devolver+" "+pdf;
                }
            },
            {
                targets: [-2],
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
            {
                targets: [-3],
                render: function (data, type, row) {
                    return pad(data, 10);
                }
            }
        ],
        createdRow: function (row, data, dataIndex) {
            if (data[6] === 'FINALIZADA') {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-success');
            } else if (data[6] === 'DEVUELTA') {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-danger');
                $('td', row).eq(7).find('a[rel="devolver"]').hide();
                $('td', row).eq(7).find('a[rel="pdf"]').hide();
            }

        }
    });

    $('#datatable tbody').on('click', 'a[rel="devolver"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['5']};
        save_estado('Alerta',
            '/venta/estado', 'Esta seguro que desea devolver esta venta?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al devolver la venta', 'far fa-smile-wink', function () {
                    datatable.ajax.reload(null, false);
                })
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
                {data: 'subtotal'}
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

function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
}
