var tblasig_insumo;
var asignar = {
    items: {
        fecha_asig: '',
        cantero: '',
        periodo: '',
        insumos: [],
    },
    add: function (data) {
        this.items.insumos.push(data);
        this.list();
    },
    list: function () {
        tblasig_insumo = $("#tblinsumos").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            scrollX: true,
            // language: {
            //     "url": '../static/lib/datatables-1.10.20/spanish.txt'
            // },
            data: this.items.insumos,
            columns: [
                {data: 'id'},
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "stock"},
                {data: "cantidad"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';

                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                }],
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data['stock'],
                    step: 1
                });
            }
        });
    }
};
$(function () {
    //texto de los selects
    $('.select2').select2({
        "language": {
            "noResults": function () {
                return "Sin resultados";
            }
        },
        allowClear: true
    });
    //seleccionar producto del select producto
    $('#id_insumo').on('select2:select', function (e) {
        var crud = $('input[name="crud"]').val();
        $.ajax({
            type: "POST",
            url: crud,
            data: {
                "id": $('#id_insumo option:selected').val(),
            },
            dataType: 'json',
            success: function (data) {
                asignar.add(data['0']);
                $('#id_insumo option:selected').remove();
            },
            error: function (xhr, status, data) {
                alert(data['0']);
            },

        })
    });
    //cantidad de productos
    $('#tblinsumos tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblasig_insumo.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este insumo de tu detalle?', function () {
                var p = asignar.items.insumos[tr.row];
                asignar.items.insumos.splice(tr.row, 1);
                $('#id_insumo').append('<option value="' + p.id + '">' + p.nombre + ' / ' + p.presentacion.nombre + '</option>');
                menssaje_ok('Confirmacion!', 'Insumo eliminado', 'far fa-smile-wink', function () {
                    asignar.list();
                });
            })
    }).on('change keyup', 'input[name="cantidad"]', function () {
        var cantidad = parseInt($(this).val());
        var tr = tblasig_insumo.cell($(this).closest('td, li')).index();
        asignar.items.insumos[tr.row].cantidad = cantidad;
    });
    $('.btnRemoveall').on('click', function () {
        if (asignar.items.insumos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los insumo seleccionados?', function () {
                asignar.items.insumos = [];
                menssaje_ok('Confirmacion!', 'Insumos eliminados', 'far fa-smile-wink', function () {
                    asignar.list();
                });
            });
    });

    $('#save').on('click', function () {
        if ($('select[name="cantero"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un cantero", 'far fa-times-circle');
            return false
        } else if (asignar.items.insumos.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un insumo", 'far fa-times-circle');
            return false
        }
        var action = $('input[name="action"]').val();
        var key = $('input[name="key"]').val();
        var parametros;
        asignar.items.fecha_asig = $('input[name="fecha_asig"]').val();
        asignar.items.periodo = $('#id_periodo').val();
        asignar.items.cantero = $('#id_cantero option:selected').val();
        if (action === 'edit') {
            parametros = {'asignar': JSON.stringify(asignar.items)};
            parametros['action'] = action;
            parametros['key'] = key;
            save_with_ajax('Alerta',
                '../../asig_insumo/editar_save', 'Esta seguro que desea editar esta asignacion?', parametros, function () {
                    location.href = '../../asig_insumo/lista';
                });
        } else {
            parametros = {'asignar': JSON.stringify(asignar.items)};
            console.log(parametros);
            save_with_ajax('Alerta',
                '/asig_insumo/crear', 'Esta seguro que desea guardar esta asignacion?', parametros, function () {
                    location.href = '/asig_insumo/lista';
                });
        }
    });
});

