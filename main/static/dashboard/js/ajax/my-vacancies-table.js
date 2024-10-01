// Table configuratusins
$(document).ready(function() {
    var dataTable = $(".datatable").DataTable({
        dom: 'rt<"bottom"ilp>',
        lengthMenu: [10, 25, 50, 100],
        scrollX: true,
        pageLength: 10,
        autoWidth: false,
        columnDefs: [
            { width: "250px", targets: 1 }
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
            { "data": null,
                "render": function (data, type, row) {
                    return `
                        <div data-toggle="tooltip" data-placement="left" title="Salary Min: ${row[7]}<br>Salary Max: ${row[4]}">${row[5]}</div>
                    `;
                }
            },
            { "data": 8 },
            {   
                "data": null,
                "render": function (data, type, row) {
                    if (row[12] == 'STANDARD'){
                        return `<div class="badge badge-soft-primary font-size-12">Standard</div>`;
                    }else{
                        return `<div class="badge badge-soft-info font-size-12">Premium</div>`;
                    }
                },
            },
            { 
                "data": null,
                "render": function (data, type, row) {
                    if (row[11]){
                        return `<div class="badge badge-soft-success font-size-12">Active</div>`;
                    };

                    return `<div class="badge badge-soft-danger font-size-12">Deactivate</div>`;
                },
            },
            {   "data": null,
                "render": function (data, type, row) {
                    if (row[13] == 'PUBLISHED'){
                        return `<div class="badge badge-soft-success font-size-12">Published</div>`;
                    }else if (row[13] == 'PENDING') {
                        return `<div class="badge badge-soft-warning font-size-12">Pending</div>`;
                    }
                    return `<div class="badge badge-soft-danger font-size-12">Deactivated</div>`;
                },
            },
            {
                "data": null,
                "render": function (data, type, row) {
                    return `
                    <div class="justify-content-center d-flex">
                        <a href="javascript:void(0);" data-id="${row[9]}" class="text-primary" data-toggle="modal" data-target=".bs-payment-detail-modal"><i class="ri-refund-2-line font-size-24"></i></a>
                    </div>`;
                }
            },
            {
                "data": null,
                "render": function (data, type, row) {
                    return `
                        <a href="/dashboard/employer/vacancy/edit/${row[9]}" class="mr-3 text-primary" data-toggle="tooltip" data-placement="top"><i class="mdi mdi-pencil font-size-18"></i></a>
                        <a href="javascript:void(0);" data-id="${row[9]}" class="text-danger delete-row" data-toggle="tooltip" data-placement="top"><i class="mdi mdi-trash-can font-size-18"></i></a>
                    `;
                }
            }
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

// const pricingTable = document.querySelectorAll('#pricing-table input');
const employerDiscountCode = document.getElementById('employer-discount-code').textContent;
const discountCode = document.getElementById('discount-code');
const totalPrice = document.getElementById('total-price');
const discountCodeInput = document.getElementById('discount-code-input');
const priceRadios = document.querySelectorAll("input[name='pricing-radio']");
const selectedOption = document.querySelector('.job-list-menu .nav-link.active');

// If the employer has a discount code, it will be automatically adapted.
if (employerDiscountCode) {
    let discountRadio = document.querySelector("input[value='Discounted']");
    discountRadio.checked = true
    discountCodeInput.style.display = 'flex';
    discountCode.value = employerDiscountCode;
}

priceRadios.forEach(radio => {
    radio.addEventListener('change', () => {
        calculatePrice();
        if (radio.value == 'Discounted') {
            discountCodeInput.style.display = 'flex';
            discountCode.value = employerDiscountCode;
        }else {
            discountCodeInput.style.display = 'none';
        }
    })
})

const calculatePrice = () => {
    setTimeout(function() {
        const priceCol = document.querySelector('.job-list-menu .nav-link.active').getAttribute('data-value');
        const hotVacancy = document.getElementById('hot-vacancy').checked;
        const priceRow = document.querySelector("input[name='pricing-radio']:checked");
        let totalPriceValue = priceRow.getAttribute(`data-${priceCol}`);

        if (hotVacancy) {
            const hotVacancyValue = priceRow.getAttribute('data-hot');
            totalPriceValue = parseInt(totalPriceValue) + parseInt(hotVacancyValue);
        }

        totalPrice.innerText = totalPriceValue;
    }, 50);
}

calculatePrice();