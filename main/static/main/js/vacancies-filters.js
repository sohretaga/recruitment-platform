const csrf_token = document.getElementById('csrf-token').value;
const slider = document.getElementById('slider1');
const url = new URL(window.location);

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrf_token);
        $('body').css('cursor', 'wait');
    },
    complete: function () {
        $('body').css('cursor', 'default');
    },
    error: function () {
        tableConsole.innerText = 'Failure when operation performed...';
    }
});

class DataCollector {

    getSalaryRangeValue() {
        const lowerValue = parseInt(document.querySelector('.noUi-handle-lower').getAttribute('aria-valuenow'));
        const upperValue = parseInt(document.querySelector('.noUi-handle-upper').getAttribute('aria-valuenow'));
        const salaryRangeList = lowerValue || upperValue ? [lowerValue, upperValue]: [];
        setUrl('salary_range', salaryRangeList.join(','));

        return salaryRangeList;
    };

    getWorkExperiences() {
        const checkboxes = document.querySelectorAll('#experience input[type="checkbox"]');
        const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);
        setUrl('work_experiences', selectedValues.join(','));

        return selectedValues;

    };

    getEmploymentTypes() {
        const checkboxes = document.querySelectorAll('#jobtype input[type="checkbox"]');
        const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);
        setUrl('employment_type', selectedValues.join(','))

        return selectedValues;

    };

    collectData() {
        const data = {
            salary_range_lower: this.getSalaryRangeValue()[0],
            salary_range_upper: this.getSalaryRangeValue()[1],
            work_experiences: this.getWorkExperiences(),
            employment_type: this.getEmploymentTypes()
        };

        return data;
    };
};

const setUrl = (parameter, value) => {
    const query_parameter = url.searchParams.has(parameter);

    if (value) {
        if (query_parameter) {
            url.searchParams.set(parameter, value);
        } else {
            url.searchParams.append(parameter, value);
        };

    } else {
        url.searchParams.delete(parameter);
    };

    window.history.pushState('', '', url);
};

const getUrlParameterValue = (parameterName) => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const parameterValue = urlParams.get(parameterName);

    return parameterValue;
};

const generatePagination = (paginationInfo) => {
    const container = document.getElementById('pagination-container');
    container.innerHTML = ''; // Clear existing content

    const currentPage = paginationInfo.current_page;
    const numPages = paginationInfo.num_pages;
    const hasPrevious = paginationInfo.has_previous;
    const hasNext = paginationInfo.has_next;

    const jobListParam = url.hash.includes('#job-list') ? '' : '#job-list';

    // Previous button
    if (hasPrevious) {
        setUrl('page', currentPage); // currentPage - 1
        const previousItem = document.createElement('li');
        previousItem.className = 'page-item';
        previousItem.innerHTML = `<a class="page-link" href="${url}${jobListParam}" tabindex="-1"><i class="mdi mdi-chevron-double-left fs-15"></i></a>`;
        container.appendChild(previousItem);
    };

    // Page numbers
    for (let i = 1; i <= numPages; i++) {
        if (i === 1 || i === numPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            setUrl('page', i);
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a class="page-link" href="${url}${jobListParam}">${i}</a>`;
            container.appendChild(pageItem);
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            const dotsItem = document.createElement('li');
            dotsItem.className = 'page-item';
            dotsItem.innerHTML = `<a class="page-link" href="${url}${jobListParam}">...</a>`;
            container.appendChild(dotsItem);
        };
    };

    // Next button
    if (hasNext) {
        setUrl('page', currentPage); // currentPage + 1
        const nextItem = document.createElement('li');
        nextItem.className = 'page-item';
        nextItem.innerHTML = `<a class="page-link" href="${url}${jobListParam}"><i class="mdi mdi-chevron-double-right fs-15"></i></a>`;
        container.appendChild(nextItem);
    };
};

const listVacancies = (vacanciesInfo) => {
    const container = document.getElementById('job-list-container');
    container.innerHTML = ''; // Clear existing content

    for (const [key, vacancy] of Object.entries(vacanciesInfo)) {
        container.innerHTML += `
        <div class="job-box bookmark-post card mt-5">
            <div class="p-4">
                <div class="row">
                    <div class="col-lg-1">
                        <a href="company-details.html"><img src="/static/main/images/featured-job/img-01.png" alt="" class="img-fluid rounded-3"></a>
                    </div><!--end col-->
                    <div class="col-lg-10">
                        <div class="mt-3 mt-lg-0">
                            <h5 class="fs-17 mb-1"><a href="/vacancy" class="text-dark">${vacancy.job_title}</a> <small class="text-muted fw-normal">(0-2 Yrs Exp.)</small></h5>
                            <ul class="list-inline mb-0">
                                <li class="list-inline-item">
                                    <p class="text-muted fs-14 mb-0">${vacancy.organization}</p>
                                </li>
                                <li class="list-inline-item">
                                    <p class="text-muted fs-14 mb-0"><i class="mdi mdi-map-marker"></i>${vacancy.location}</p>
                                </li>
                                <li class="list-inline-item">
                                    <p class="text-muted fs-14 mb-0"><i class="uil uil-wallet"></i>${vacancy.salary_minimum} ₼ - ${vacancy.salary_maximum} ₼ / month</p>
                                </li>
                            </ul>
                            <div class="mt-2">
                                <span class="badge bg-soft-success mt-1">Full Time</span>
                                <span class="badge bg-soft-warning mt-1">Urgent</span>
                                <span class="badge bg-soft-info mt-1">Private</span>
                            </div>
                        </div>
                    </div><!--end col-->
                </div><!--end row-->
                <div class="favorite-icon">
                    <a href="javascript:void(0)"><i class="uil uil-heart-alt fs-18"></i></a>
                </div>
            </div>
            <div class="p-3 bg-light">
                <div class="row justify-content-between">
                    <div class="col-md-8">
                        <div>
                            <ul class="list-inline mb-0">
                                <li class="list-inline-item"><i class="uil uil-tag"></i> Keywords :</li>
                                <li class="list-inline-item"><a href="javascript:void(0)" class="primary-link text-muted">Ui designer</a>,</li>
                                <li class="list-inline-item"><a href="javascript:void(0)" class="primary-link text-muted">developer</a></li>
                            </ul>
                        </div>
                    </div>
                    <!--end col-->
                    <div class="col-md-3">
                        <div class="text-md-end">
                            <a href="#applyNow" data-bs-toggle="modal" class="primary-link">Apply Now <i class="mdi mdi-chevron-double-right"></i></a>
                        </div>
                    </div>
                    <!--end col-->
                </div>
                <!--end row-->
            </div>
        </div>`
    };

};

// Filter Request
const filterRequest = () => {
    const data = new DataCollector();
    const collectded_data = data.collectData();

    $.ajax({
        url: `/ajax/filter-vacancies`,
        type: 'POST',
        data: JSON.stringify(collectded_data),
        success: (response) => {
            listVacancies(response.vacancies);
            generatePagination(response.pagination);
        }

    });
};

// Salary Range Listener
slider.noUiSlider.on('change', filterRequest);

const addCheckboxListener = (selector, callback) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', callback);
    });
};

const setFilterCheckboxes = (selector, values) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        if (values.includes(checkbox.value)) {
            checkbox.checked = true;
        };
    });
};

addCheckboxListener('#experience input[type="checkbox"]', filterRequest); // Work Experiences Listener
addCheckboxListener('#jobtype input[type="checkbox"]', filterRequest); // Type of Employment Listener

// Set filter inputs from url parameters
try {
    slider.noUiSlider.set(getUrlParameterValue('salary_range').split(','));
    setFilterCheckboxes('#experience input[type="checkbox"]', getUrlParameterValue('work_experiences').split(',')); // Set work experience
    setFilterCheckboxes('#jobtype input[type="checkbox"]', getUrlParameterValue('employment_type').split(',')); // Set type of employment
} catch (error) { };