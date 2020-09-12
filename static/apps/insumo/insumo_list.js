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
$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        destroy: true,
        autoWidth: false,
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
        dom: '<"top"B><br>frtip',
        buttons:[
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
                orientation: 'portrait', //landscape', //portrait
                pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                download: 'open',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6],
                    search: 'applied',
                    order: 'applied'
                },
                customize: function (doc) {
                    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                        "Septiembre", "Octubre",
                        "Noviembre", "Diciembre"
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
                    // var logo = logotipo;
                    //[izquierda, arriba, derecha, abajo]
                    doc.pageMargins = [25, 120, 0, 50];
                    doc.defaultStyle.fontSize = 11;
                    doc.styles.tableHeader.fontSize = 12;
                    doc['header'] = (function () {
                        return {
                            columns: [{alignment: 'center', image: logotipo, width: 300}],
                            margin: [190, 20, 0, 0] //[izquierda, arriba, derecha, abajo]
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

                    doc.content[1].table.widths = [30, 120, 60, 140, 80, 40, 40];
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
                }
            },
            {
                text: '<i class="fa fa-file-excel"> Reporte Excel</i>', className: "btn btn-success btn-round my_class",
                extend: 'excel'
            }
        ],
        ajax: {
            url: '/insumo/ajax',
            type: 'POST',
            dataSrc: "",
        },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a rel="edit" href="/insumo/editar/' + row[0] + '" type="button" class="btn btn-primary btn-sm btn-flat btn-round" style="color: white" data-toggle="tooltip" title="Editar Insumo"><i class="fa fa-edit"></i></a>' + ' ';
                    var del = '<a rel="del" type="button" class="btn btn-danger btn-sm btn-flat btn-round" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                    return edit + del;
                }
            },
            {
                searchPanes: {
                    show: true,
                },
                targets: [0, 1, 2, 3, 4, 5, 6],
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$ ' + parseFloat(data).toFixed(2);
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
            if (data[6] <= 0) {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-danger');
            } else if (data[6] < 50) {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-warning');
            } else if (data[6] >= 21) {
                $('td', row).eq(6).find('span').addClass('badge badge-pill badge-success');
            }

        }

    });

    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/insumo/eliminar', 'Esta seguro que desea eliminar este insumo?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el insumo!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});