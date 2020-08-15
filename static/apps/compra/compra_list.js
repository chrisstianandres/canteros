$(function () {
            $("#datatable").DataTable({
                responsive: true,
                autoWidth: false,
                // language: {
                //     "url": '../static/lib/datatables-1.10.20/spanish.txt'
                // },

                createdRow: function (row, data, dataIndex) {
                    console.log(data[4]);
                    if (data[4] === '<span>FINALIZADA</span>') {
                        $('td', row).eq(4).find('span').addClass('badge badge-pill badge-success');
                        $('td', row).eq(5).find('button[name="btnestado"]').prop('disabled', true);
                    } else if (data[4] === '<span>PENDIENTE</span>') {
                        $('td', row).eq(4).find('span').addClass('badge badge-pill badge-warning');
                        //console.log($('td', row).eq(4).find('span').addClass('badge badge-pill badge-success'));
                        //$('td', row).eq(4).addClass('badge badge-pill badge-danger');
                    }

                }

            });
        });