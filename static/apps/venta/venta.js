var tblventa;
var ventas = {
    items: {
        fecha_venta: '',
        cliente: '',
        subtotal: 0.00,
        iva: 0.00,
        iva_emp: 0.00,
        total: 0.00,
        productos: [],
    },
    calculate: function () {
        var subtotal = 0.00;
        var iva_emp = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            console.clear();
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
    add: function (data) {
        this.items.productos.push(data);
        this.list();
    },
    list: function () {
        this.calculate();
        tblventa = $("#tblproductos").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            scrollX: true,
            // language: {
            //     "url": '../static/lib/datatables-1.10.20/spanish.txt'
            // },
            data: this.items.productos,
            columns: [
                {data: 'id'},
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "stock"},
                {data: "cantidad"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Producto"><i class="fa fa-trash-alt"></i></a>';
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
                    max: data['stock'],
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
    $('#id_producto').on('changed.bs.select', function (e) {
        var crud = $('input[name="crud"]').val();
        $.ajax({
            type: "POST",
            url: crud,
            data: {
                "id": $('#id_producto option:selected').val(),
            },
            dataType: 'json',
            success: function (data) {
                ventas.add(data['0']);
                $('#id_producto option:selected').remove();
                $('#id_producto').selectpicker('refresh');
            },
            error: function (xhr, status, data) {
                alert(data['0']);
            },

        })
    });
    //cantidad de productos
    $('#tblproductos tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblventa.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este producto de tu detalle?', function () {
                var p = ventas.items.productos[tr.row];
                ventas.items.productos.splice(tr.row, 1);
                $('#id_producto').append('<option value="'+p.id+'">'+p.nombre+'</option>');
                $('#id_producto').selectpicker('refresh');

                menssaje_ok('Confirmacion!', 'Producto eliminado', 'far fa-smile-wink', function () {
                    ventas.list();
                });
            })
    })
        .on('change keyup', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = tblventa.cell($(this).closest('td, li')).index();
            ventas.items.productos[tr.row].cantidad = cantidad;
            ventas.calculate();
            $('td:eq(7)', tblventa.row(tr.row).node()).html('$' + ventas.items.productos[tr.row].subtotal.toFixed(2));
        });
    $('.btnRemoveall').on('click', function () {
        if (ventas.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos seleccionados?', function () {
                ventas.items.productos = [];
                menssaje_ok('Confirmacion!', 'Productos eliminados', 'far fa-smile-wink', function () {
                    location.reload();
                });
            });
    });

    $('#save').on('click', function () {
        if ($('select[name="cliente"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un cliente", 'far fa-times-circle');
            return false
        } else if (ventas.items.productos.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
            return false
        }
        var action = $('input[name="action"]').val();
        var key = $('input[name="key"]').val();
        var parametros;
        ventas.items.fecha_venta = $('input[name="fecha_venta"]').val();
        ventas.items.cliente = $('#id_cliente option:selected').val();
        if (action === 'edit') {
            parametros = {'ventas': JSON.stringify(ventas.items)};
            parametros['action'] = action;
            parametros['key'] = key;
            save_with_ajax('Alerta',
                '../../venta/editar_save', 'Esta seguro que desea editar esta venta?', parametros, function () {
                    location.href = '../../venta/lista';
                });
        } else {
            parametros = {'ventas': JSON.stringify(ventas.items)};
            save_with_ajax('Alerta',
                '/venta/crear', 'Esta seguro que desea guardar esta venta?', parametros, function () {
                    location.href = '/venta/lista';
                });
        }
    });
});

