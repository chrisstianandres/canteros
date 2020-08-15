var tblcompra;
var compras = {
    items: {
        fecha_compra: '',
        proveedor: '',
        subtotal: 0.00,
        iva: 0.00,
        iva_emp: 0.00,
        total: 0.00,
        insumos: [],
    },
    calculate: function () {
        var subtotal = 0.00;
        var iva_emp = 0.00;
        $.each(this.items.insumos, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
            iva_emp = dict.iva_emp;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva_emp;
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));

    },
    add: function (response) {
        this.items.insumos.push(response);
        this.list();
    },

    list: function () {
        this.calculate();
        tblcompra = $("#tblinsumos").DataTable({
            responsive: true,
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            language: {
                "url": '../static/lib/datatables-1.10.20/spanish.txt'
            },
            data: this.items.insumos,
            columns: [
                {data: 'id'},
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "cantidad"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            columnDefs: [{
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                    //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';

                }
            },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                }],
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 1
                });
            }
        });
    }
};
$(function () {
    //texto de los selects
    $('.selectpicker').selectpicker({
        noneResultsText: 'Sin resultados'
    });
    //seleccionar producto del select producto
    $('#id_insumo').on('change', function (e) {
        var id = $("#id_insumo").val();
        if (id) {
            var request = $.ajax({
                type: "POST",
                url: "../compra/get_insumo",
                data: {
                    "id": id
                },
            });
            request.done(function (response) {
                e.stopPropagation();
                compras.add(response['0']);
                $('#id_insumo').val('').trigger('change');
            });
            request.fail(function (response) {
                alert(response.data.error)

            })
        }
    });
    //cantidad de productos
    $('#tblinsumos tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblcompra.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación' + ' ' + '<i class="fas fa-exclamation-triangle"></i>',
            'Esta seguro que desea eliminar este producto de tu detalle?', function () {
                compras.items.insumos.splice(tr.row, 1);
                compras.list();
            });
    })
        .on('change', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = tblcompra.cell($(this).closest('td, li')).index();
            compras.items.insumos[tr.row].cantidad = cantidad;
            compras.calculate();
            $('td:eq(6)', tblcompra.row(tr.row).node()).html('$' + compras.items.insumos[tr.row].subtotal.toFixed(2));
        });
    $('.btnRemoveall').on('click', function () {
        if (compras.items.insumos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación' + ' ' + '<i class="fas fa-exclamation-triangle"></i>',
            'Esta seguro que desea eliminar todos los productos seleccionados?', function () {
                compras.items.insumos = [];
                compras.list();
            });
    });

    $('#save').on('click', function () {
        if ($('select[name="proveedor"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un proveedor", 'far fa-times-circle');
            return false
        }
        else
            if(compras.items.insumos.length === 0){
                menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
            return false
            }
        compras.items.fecha_compra = $('input[name="fecha_compra"]').val();
        compras.items.proveedor = $('select[name="proveedor"]').val();
        var parametros = {'compras': JSON.stringify(compras.items)};
        console.log(parametros);
        save_with_ajax('Alerta' + ' ' + '<i class="fas fa-exclamation-triangle"></i>',
            '/compra/crear', 'Esta seguro que desea guardar esta compra?', parametros, function () {
                location.href = '/compra/lista';
            });
    })

});

function borrar_todo_alert(title, content, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    callback();
                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}

function save_with_ajax(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                    //

                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {
                    callback();
                }
            }
        }
    });
}

function menssaje_error(title, content, icon) {
    $.confirm({
        theme: 'modern',
        icon: icon,
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue',
            },
        }
    });
}

