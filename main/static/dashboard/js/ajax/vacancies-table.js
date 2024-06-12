// Table configuratusins
$(document).ready(function() {
    var dataTable = $(".datatable").DataTable({
        lengthMenu: [10, 25, 50, 100],
        pageLength: 10,
        columns: columns = [
            { orderable: false },
            { orderable: false },
            { orderable: false },
            { orderable: false },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: false }
        ],
        order: [[1, "asc"]],
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/dashboard/ajax/vacancies",
            "type": "GET"
        },
        "columns": [
            { "data": null,
                "render": function (data, type, row) {
                    return `<a href="/vacancy/${row[10]}" class="text-dark font-weight-bold" target='_blank'>${row[0]}</a>`;
                }
            },
            { "data": 1 },
            { "data": 2 },
            { "data": 3 },
            { "data": 4 },
            { "data": 5 },
            { "data": 6 },
            { "data": 7 },
            { "data": 8 },
            {   "data": null,
                "render": function (data, type, row) {
                    if (row[11]){
                        return `<div class="badge badge-soft-success font-size-12">Active</div>`;
                    };

                    return `<div class="badge badge-soft-danger font-size-12">Deactivate</div>`;
                },
            },
            {
                "data": null,
                "render": function (data, type, row) {
                    return `
                        <a href="/dashboard/vacancy/edit/${row[9]}" class="mr-3 text-primary" data-toggle="tooltip" data-placement="top"><i class="mdi mdi-pencil font-size-18"></i></a>
                        <a href="javascript:void(0);" data-id="${row[9]}" class="text-danger delete-row" data-toggle="tooltip" data-placement="top"><i class="mdi mdi-trash-can font-size-18"></i></a>
                    `;
                }
            }
        ],
        
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        }
    });

    $('.datatable').on('click', '.delete-row', function(e) {
        e.preventDefault();

        var row = $(this).closest('tr');
        var dataId = $(this).data('id');

        Swal.fire({
            title: "Are you sure?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Yes, delete it!"
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/dashboard/ajax/delete-vacancy',
                    method: 'POST',
                    data: { vacancy_id: dataId },
                    success: function(response) {
                        dataTable.row(row).remove().draw();
                    },
                    error: function(xhr, status, error) {
                        console.log('Error:', error);
                    }
                });

              Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Item has been deleted!",
                showConfirmButton: false,
                timer: 1000
              });
            }
          });
    });
});
