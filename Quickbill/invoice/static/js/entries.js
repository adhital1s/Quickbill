$(document).ready(function () {
    $('.table').DataTable({
        "pagingType": "simple",

        lengthMenu: [
            [15, 25, 100, -1],
            [15, 25, 100, "All"]
        ],
        pageLength: 100,
        dom: 'lBfrtip',
        buttons: [{
            extend: 'collection',
            text: 'Export',
            align: 'right',
            buttons: [
                'copy',
                'excel',
                'csv',
                'pdf',
                'print'
            ]
        }],
    })
})