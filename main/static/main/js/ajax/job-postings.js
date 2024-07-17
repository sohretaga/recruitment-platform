const deleteVacancyBtn = document.getElementById('delete-vacancy-btn');
const deleteVacancyModal = new bootstrap.Modal(document.getElementById('deleteVacancyModal'));
const vacancyCount = document.getElementById('vacancy-count');
const url = new URL(window.location);

const filterOrderby = new Choices('#filter-orderby', {
    shouldSort: false,
    shouldSortItems: false,
    searchEnabled: false
});

$('#deleteVacancyModal').on('hidden.bs.modal', function(e) {
    deleteVacancyBtn.removeAttribute('onclick');
});

const deleteRequest = (id) => {
    deleteVacancyBtn.setAttribute('onclick', `deleteVacancy(${id})`);
    deleteVacancyModal.show();
};

const deleteVacancy = (id) => {
    $.ajax({
        url:'/dashboard/ajax/delete-vacancy',
        type: 'POST',
        data: {vacancy_id: id},
        success: function(response) {
            document.getElementById(`vacancy-${id}`).remove();
            deleteVacancyModal.hide();
        }
    });
};

const setUrl = (parameter, value) => {
    const queryParameter = url.searchParams.has(parameter);
    if (value) {
        if (queryParameter) {
            url.searchParams.set(parameter, value);
        } else {
            url.searchParams.append(parameter, value);
        };

    } else {
        if (queryParameter) {
            url.searchParams.delete(parameter);
        };
    };

    window.history.pushState('', '', url);
};

const generatePagination = (paginationInfo) => {
    const container = document.getElementById('pagination-container');
    container.innerHTML = ''; // Clear existing content

    const currentPage = paginationInfo.current_page;
    const numPages = paginationInfo.num_pages;
    const hasPrevious = paginationInfo.has_previous;
    const hasNext = paginationInfo.has_next;
    const separator = url.searchParams.size ? '&':'?'; // return & or ? symbol

    setUrl('page'); // delete page parameter from url

    // Previous button
    if (hasPrevious) {
        const previousItem = document.createElement('li');
        previousItem.className = 'page-item';
        previousItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${currentPage - 1}" tabindex="-1"><i class="mdi mdi-chevron-double-left fs-15"></i></a>`;
        container.appendChild(previousItem);
    };

    // Page numbers
    for (let i = 1; i <= numPages; i++) {
        if (i === 1 || i === numPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${i}">${i}</a>`;
            container.appendChild(pageItem);
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            const dotsItem = document.createElement('li');
            dotsItem.className = 'page-item';
            dotsItem.innerHTML = `<a class="page-link" href="${url}">...</a>`;
            container.appendChild(dotsItem);
        };
    };

    // Next button
    if (hasNext) {
        const nextItem = document.createElement('li');
        nextItem.className = 'page-item';
        nextItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${currentPage + 1}"><i class="mdi mdi-chevron-double-right fs-15"></i></a>`;
        container.appendChild(nextItem);
    };

};

const listVacancies = (vacanciesInfo) => {
    const container = document.getElementById('job-list-container');
    container.innerHTML = ''; // Clear existing content

    for (const [key, vacancy] of Object.entries(vacanciesInfo)) {
        container.innerHTML += `
        <div id="vacancy-${vacancy.id}" class="job-box card mt-4">
            <div class="card-body p-4">
                <div class="row">
                    <div class="col-lg-1">
                        <a href="/company/${vacancy.employer_username}"><img src="${vacancy.profile_photo_url ? `${vacancy.profile_photo_url}`:'/static/main/images/featured-job/default-company-img.jpeg'}" alt="${vacancy.company_name}" class="img-fluid rounded-3"  width="70"></a>
                    </div>
                    <div class="col-lg-7 d-flex">
                        <div class="mt-3 mt-lg-0">
                            <h5 class="fs-17 mb-1"><a href="/vacancy/${vacancy.slug}" class="text-dark">${vacancy.position_title}</a> ${vacancy.status ? '':'<span class="badge bg-soft-danger mt-1">Deactive</span>'}</h5>
                            <ul class="list-inline mb-0">
                                <li class="list-inline-item">
                                    <p class="text-muted fs-14 mb-0">${vacancy.company_name}</p>
                                </li>
                                <li class="list-inline-item">
                                    <p class="text-muted fs-14 mb-0"><i class="mdi mdi-map-marker"></i> ${vacancy.location_name}</p>
                                </li>
                                <li class="list-inline-item">
                                    <p class="text-muted fs-14 mb-0"><i class="uil uil-wallet"></i> ${vacancy.salary_minimum} ₼ - ${vacancy.salary_maximum} ₼ / month</p>
                                </li>
                            </ul>
                            <div class="mt-2">
                                <!-- <span class="badge bg-soft-danger mt-1">Part Time</span> -->
                                <span class="badge bg-soft-warning mt-1">Urgent</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4 align-self-center">
                        <ul class="list-inline mt-3 mb-0">
                            <li class="list-inline-item" data-bs-toggle="tooltip" data-bs-placement="top">
                                <a href="{% url 'job:applicants' vacancy.slug %}" class="btn btn-primary ${vacancy.application_count ? '':'disabled'}">Applicants (${vacancy.application_count}) <i class="uil uil-folder-open"></i></a>
                            </li>
                            <li class="list-inline-item" data-bs-toggle="tooltip" data-bs-placement="top" title="Edit">
                                <a href="{% url 'dashboard:edit-vacancy' vacancy.id %}" class="avatar-sm bg-soft-success d-inline-block text-center rounded-circle fs-18">
                                    <i class="uil uil-edit"></i>
                                </a>
                            </li>
                            <li class="list-inline-item" data-bs-toggle="tooltip" data-bs-placement="top" title="Delete">
                                <a href="javascript:void(0)" class="avatar-sm bg-soft-danger d-inline-block text-center rounded-circle fs-18" onclick="deleteRequest('{{ vacancy.id }}')"><i class="uil uil-trash-alt"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div><!--end row-->
            </div>
        </div>`;
    };
};

document.querySelector('#filter-orderby').addEventListener('change', (option) => {
    const selectedValue = option.target.value;
    setUrl('orderby', selectedValue);

    $.ajax({
        url: '/ajax/ajax-filter-job-postings',
        type: 'POST',
        data: {filter_orderby: selectedValue},
        success: function(response) {
            vacancyCount.innerText = response.vacancy_count;

            generatePagination(
                response.pagination
            );

            listVacancies(
                response.vacancies
            )
        }
    });
});