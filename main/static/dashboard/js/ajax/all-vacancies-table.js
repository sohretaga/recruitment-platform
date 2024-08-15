// Table configuratusins
$(document).ready(function() {
    var dataTable = $(".datatable").DataTable({
        lengthMenu: [10, 25, 50, 100],
        pageLength: 10,
        columnDefs: [
            { width: '250px', targets: 0 },
            { width: '200px', targets: 1 },
            { width: '100px', targets: 2 },
            { width: '100px', targets: 3 },
            { width: '70px', targets: 4 },
            { width: '70px', targets: 5 },
            { width: '80px', targets: 6 },
            { width: '50px', targets: 7 },
            { width: '50px', targets: 8 },
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
            { "data": 2 },
            { "data": 3 },
            { "data": 4 },
            { "data": 5 },
            { "data": 6 },
            { "data": 7 },
            { "data": 8 },
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
            }
        ],
        
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        }
    });

});


const setApprovalLevel = (event, id) => {
    let value = event.value;
    $.ajax({
        url: '/dashboard/controller/ajax/manage-approval-level',
        type: 'POST',
        data: {
            vacancy_id: id,
            approval_level: value
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