var tblasig_labor;
var ingresar = {
    items: {
        fecha: '',
        periodo: '',
        canteros: [],
    },
    add: function (data) {
        this.items.canteros.push(data);
        // this.list();
    },
    save: function () {
        var parametros = {'ingresos': JSON.stringify(this.items)};
        console.log(parametros);
        save_with_ajax('Guardar Ingresos de Produccion', '/produccion/save', '¿Esta seguro que desea guardar este ingreso de produccion?', parametros, function () {
            location.href = '/produccion/lista';
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
                    return '<input type="text" name= "cantidad" class="form-control form-control-sm input-sm col-sm-10" value="1">';
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
        rowCallback: function (row, data) {
            $(row).find('input[name="cantidad"]').TouchSpin({
                min: 1,
                max: 99999999999999,
                step: 1
            });
        }
    });
    $('#save').on('click', function () {

        ingresar.items.fecha = $('input[name="fecha"]').val();
        ingresar.items.periodo = $('select[name="periodo"] option:selected').val();
        var trs = $("#tbltrab tr").length;
        $("#tbltrab tbody tr").each(function (index) {
            var c, p, ct;
            var filas = $(this).children("td").each(function (index2) {
                switch (index2) {
                    case 0:
                        c = $(this).text();
                        break;
                    case 1:
                        break;
                    case 2:
                        p = $(this).find('select[name="producto"] option:selected').val();
                        break;
                    case 3:
                        ct = $(this).find('input[name="cantidad"]').val();
                        break;
                }
            });
            var items = {
                "cantero": c,
                "producto": p,
                "cantidad": ct
            };
            ingresar.add(items);
        });
        ingresar.save();
    });
});
