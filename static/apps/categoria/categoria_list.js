$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/categoria/eliminar', 'Esta seguro que desea eliminar esta categoria?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar la categoria!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});