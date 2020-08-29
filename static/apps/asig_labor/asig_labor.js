var tblasig_labor;
var asignar = {
    items: {
        fecha_asig: '',
        periodo: '',
        trabajadores: [],
    },
    add: function (data) {
        this.items.trabajadores.push(data);
        // this.list();
    },
    save: function () {
        var parametros = {'asignaciones': JSON.stringify(this.items)};
       save_with_ajax('Guardar Asignaciones', '/asig_labor/save_asig', 'Esta seguro que desea guardar las asignaciones', parametros, function () {
            location.href = '../asig_labor/lista';
       });

    }
};

$(function () {
    $('.select2').select2({
        "language": {
            "noResults": function () {
                return "Sin resultados";
            }
        },
        allowClear: true
    });
    datatable = $("#tbltrab").DataTable({
        destroy: true,
        autoWidth: false,
        dataSrc: "",
        scrollX: false,
        "searching": false,
        // language: {
        //     "url": '../static/lib/datatables-1.10.20/spanish.txt'
        // },
        columnDefs: [
            {
                targets: [-1],

                render: function (data, type, row) {
                    return '<input type="text" name= "tiempo" class="form-control col-sm-10 tiempo">';
                    // return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';
                }
            },
            {
                targets: 2,
                width: '40%'
            },
            {
                targets: 1,
                width: '30%'
            },

        ],
    });
    $('input[name="tiempo"]').daterangepicker();
    $('#save').on('click', function () {
        asignar.items.fecha_asig = $('input[name="fecha_asig"]').val();
        asignar.items.periodo = $('select[name="periodo"] option:selected').val();
        var trs = $("#tbltrab tr").length;
        $("#tbltrab tbody tr").each(function (index) {
            var t, l, d, h;
            var filas = $(this).children("td").each(function (index2) {
                switch (index2) {
                    case 0:
                        t = $(this).text();
                        break;
                    case 1:
                        break;
                    case 2:
                        l = $(this).find('select[name="labor"] option:selected').val();
                        break;
                    case 3:
                        d = $(this).find('input[name="tiempo"]').data('daterangepicker').startDate.format('YYYY-MM-DD');
                        h = $(this).find('input[name="tiempo"]').data('daterangepicker').endDate.format('YYYY-MM-DD');
                        break;
                }
            });
            var items = {
                "trabajador": t,
                "labor": l,
                "desde": d,
                "hasta": h
            };
            asignar.add(items);
        });
        asignar.save();
    });
});
