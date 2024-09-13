// Table configuratusins
$(document).ready(function() {
    var dataTable = $(".datatable").DataTable({
        dom: 'rt<"bottom"ilp>',
        lengthMenu: [10, 25, 50, 100],
        scrollX: true,
        pageLength: 10,
        ordering: false,
        columns: [
            { orderable: false },
            { orderable: false },
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

    $('.customSearch').on('keyup', function() {
        dataTable.search(this.value).draw();
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
                    url: '/dashboard/ajax/delete-comment',
                    method: 'POST',
                    data: { comment_id: dataId },
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

const setStatus = (event, id) => {
    let value = event.value;
    $.ajax({
        url: '/dashboard/ajax/manage-comment-status',
        type: 'POST',
        data: {
            comment_id: id,
            status: value
        },
        success: () => {
            event.className = '';

            if (value == 'PUBLISHED') {
                event.className = 'badge badge-soft-success font-size-12 btn dropdown-toggle';
            }else if (value == 'PENDING') {
                event.className = 'badge badge-soft-warning font-size-12 btn dropdown-toggle';
            }else if (value == 'DEACTIVATED') {
                event.className = 'badge badge-soft-danger font-size-12 btn dropdown-toggle';
            };
        }
    });
}

const saveCommentBtn = document.getElementById('save-comment-btn');
const editCommentModal = new bootstrap.Modal(document.getElementById('editCommentModal'));
const editCommentArea = document.getElementById('edit-comment-area')

$('#editCommentModal').on('hidden.bs.modal', function(e) {
    saveCommentBtn.removeAttribute('onclick');
});

const editComment = (id) => {
    let commentText = document.getElementById(`comment-text-${id}`);
    editCommentArea.innerText = commentText.innerText;

    saveCommentBtn.setAttribute('onclick', `editRequest(${id})`);
    editCommentModal.show();
};

const editRequest = (id) => {
    $.ajax({
        url:'/dashboard/ajax/edit-comment',
        type: 'POST',
        data: {
            comment_id: id,
            edited_comment: editCommentArea.value
        },
        success: () => {
            let commentText = document.getElementById(`comment-text-${id}`);
            commentText.innerText = editCommentArea.value;

            editCommentArea.innerText = '';
            editCommentModal.hide();
        }
    });
};