var pago = {
    items: {
        id: '',
        valor_pag: 0.00
    }
};

$(function () {
    $('input[name="valor_pag"]').TouchSpin({
        min: 1.00,
        max: parseFloat($('input[name="saldo"]').val()),
        step: 0.01,
        decimals: 2,
        forcestepdivisibility: 'none',
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    });
    $('#save').on('click', function () {
        var valores;
        pago.items.id=$('input[name="id"]').val();
        pago.items.valor_pag=$('input[name="valor_pag"]').val();
        valores = {'valores': JSON.stringify(pago.items)};
        save_with_ajax('Alerta', $('input[name="crud"]').val(), 'Esta seguro que desea guardar este pago?',
            valores, function () {
                    location.href = '/asig_labor/lista';
                });



    })
});