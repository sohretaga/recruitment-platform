// Table configuratusins
$(document).ready(function() {
    var dataTable = $(".datatable").DataTable({
        lengthMenu: [10, 25, 50, 100],
        pageLength: 10,
        columns: [
            { orderable: true },
            { orderable: false },
            { orderable: false }
        ],
        order: [[1, "asc"]],
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
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
                    url: '/dashboard/ajax/delete-faq',
                    method: 'POST',
                    data: { faq_id: dataId },
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