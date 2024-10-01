// Table configuratusins
$(document).ready(function() {
    var dataTable = $(".datatable").DataTable({
        dom: 'rt<"bottom"ilp>',
        lengthMenu: [10, 25, 50, 100],
        scrollX: true,
        pageLength: 10,
        autoWidth: false,
        columnDefs: [
            { width: '250px', targets: 1 },
        ],
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
            { orderable: true }
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
            "url": "/dashboard/controller/ajax/vacancies",
            "type": "GET"
        },
        "columns": [
            { "data": null,
                "render": function (data, type, row) {
                    return `<a href="/vacancy/${row[10]}" class="text-dark font-weight-bold" target='_blank'>${row[0]}</a>`;
                }
            },
            { "data": 1 },
            { "data": 14 },
            { "data": null,
                "render": function (data, type, row) {
                    return `
                        <select onchange="setApprovalLevel(this, ${row[9]})"
                            class="badge ${row[12] == 'PUBLISHED' ? 'badge-soft-success': row[12] == 'PENDING' ? 'badge-soft-warning': 'badge-soft-danger'} font-size-12 btn dropdown-toggle" >
                            <option value="PUBLISHED" ${row[12] == 'PUBLISHED' ? 'selected':''}>
                                <div class="badge badge-soft-success font-size-12">Published</div>
                            </option>
                            <option value="PENDING" ${row[12] == 'PENDING' ? 'selected':''}>
                                <div class="badge badge-soft-warning font-size-12">Pending</div>
                            </option>
                            <option value="DEACTIVATED" ${row[12] == 'DEACTIVATED' ? 'selected':''}>
                                <div class="badge badge-soft-danger font-size-12">Deactivated</div>
                            </option>
                        </select>
                    `;
                }
            },
            { "data": null,
                "render": function (data, type, row) {
                    return `
                        <select onchange="setType(this, ${row[9]})"
                            class="badge ${row[13] == 'STANDARD' ? 'badge-soft-primary':'badge-soft-info'} font-size-12 btn dropdown-toggle" >
                            <option value="STANDARD" ${row[13] == 'STANDARD' ? 'selected':''}>
                                <div class="badge badge-soft-primary font-size-12">Standard</div>
                            </option>
                            <option value="PREMIUM" ${row[13] == 'PREMIUM' ? 'selected':''}>
                                <div class="badge badge-soft-info font-size-12">Premium</div>
                            </option>
                        </select>
                    `;
                }
            },
            {  "data": null,
                "render": function (data, type, row) {
                    if (row[11]){
                        return `<div class="badge badge-soft-success font-size-12">Active</div>`;
                    };

                    return `<div class="badge badge-soft-danger font-size-12">Deactivate</div>`;
                },
            },
            { "data": 2 },
            { "data": 3 },

            { "data": null,
                "render": function (data, type, row) {
                    return `
                        <div data-toggle="tooltip" data-placement="left" title="Salary Min: ${row[4]}<br>Salary Max: ${row[6]}">${row[7]}</div>
                    `;
                }
            },

            { "data": 8 },
        ],
        
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");

            // Enable Bootstrap tooltips on every redraw
            $('[data-toggle="tooltip"]').tooltip({
                html: true
            });
        }
    });

    $('.customSearch').on('keyup', function() {
        dataTable.search(this.value).draw();
    });

});

const setType = (event, id) => {
    let value = event.value;
    $.ajax({
        url: '/dashboard/controller/ajax/manage-type',
        type: 'POST',
        data: {
            vacancy_id: id,
            type: value
        },
        success: () => {
            event.className = '';

            if (value == 'STANDARD') {
                event.className = 'badge badge-soft-primary font-size-12 btn dropdown-toggle';

            }else if (value == 'PREMIUM') {
                event.className = 'badge badge-soft-info font-size-12 btn dropdown-toggle';
            };
        }
    });
}


const setApprovalLevel = (event, id) => {
    let value = event.value;
    $.ajax({
        url: '/dashboard/controller/ajax/manage-approval-level',
        type: 'POST',
        data: {
            vacancy_id: id,
            approval_level: value
        },
        success: (response) => {
            event.className = '';

            if (value == 'PUBLISHED') {
                event.className = 'badge badge-soft-success font-size-12 btn dropdown-toggle';

                if (response.published_date) {
                    updatePublishedDate(id);
                }

            }else if (value == 'PENDING') {
                event.className = 'badge badge-soft-warning font-size-12 btn dropdown-toggle';
            }else if (value == 'DEACTIVATED') {
                event.className = 'badge badge-soft-danger font-size-12 btn dropdown-toggle';
            };
        }
    });
}


const updatePublishedDate = (vacancy_id) => {
    Swal.fire({
        title: "Update the published date?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Update"
        }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/dashboard/controller/ajax/update-published-date',
                method: 'POST',
                data: { vacancy_id: vacancy_id },
                success: () => {
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Published date updated!",
                        showConfirmButton: false,
                        timer: 1000
                    });
                },
                error: (xhr, status, error) => {
                    console.log('Error:', error);
                }
            });
        }
    });
}