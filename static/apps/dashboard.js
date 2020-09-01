var graphpie = Highcharts.chart('container', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Compras Totales del año 2020'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
});


function cahrtcompras() {
    $.ajax({
        url: '/compra/chart',
        type: 'POST',
        data: {'action': 'chart'},
        dataSrc: "",
    }).done(function (data) {
        graphpie.addSeries(data);
    });
}

function cahrtventas() {
    $.ajax({
        url: '/venta/chart',
        type: 'POST',
        data: {'action': 'chart'},
        dataSrc: "",
    }).done(function (data) {
        var yea = data['cat'];
        var chart = Highcharts.chart('container2', {
            title: {
                text: 'Ventas del año '+ '<strong>'+yea[0]+'</strong>'+ ' al año ' +'<strong>'+yea[5]+'</strong>'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>$ {point.y}</b>'
            },
            accessibility: {
                point: {
                    valueSuffix: '$'
                }
            },

            yAxis: {
                title: {
                    text: 'Valores $'
                }
            },
            xAxis: {
                categories: data['cat']
            },

        });
        chart.addSeries(data['dat']);
    });
}

$(function () {
    var datatable = $("#datatable").DataTable({
        autoWidth: false,
        dom: "tip",
        ScrollX: '90%',
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
        },
        ajax: {
            url: '/compra/index',
            type: 'POST',
            data: {'action': 'table'},
            dataSrc: "",
        },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$ ' + data;
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            $('td', row).eq(3).find('span').addClass('badge badge-pill badge-success');
        }
    });
    cahrtcompras();
    cahrtventas();

});