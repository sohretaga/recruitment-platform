const slider = document.getElementById('slider1');
const url = new URL(window.location);

// Salary Values
const [minValue, maxValue] = [0, 100000]

var workExperiencesCheckboxes = '#experience input[type="checkbox"]';
var employmentTypeCheckboxes = '#jobtype input[type="checkbox"]';
var workPreferenceCheckboxes = '#preference input[type="checkbox"]';
var departmentCheckboxes = '#department input[type="checkbox"]';
var datePostedRadios = '#dateposted input[type="radio"]';

decodeURIComponent(url);

noUiSlider.create(slider, {
    start: [minValue, maxValue],
    step: 1,
    connect: true,
    range: {
        min: [minValue],
        max: [maxValue]
    },
    format: {
        to: function (value) {
            return Math.round(value);
        },
        from: function (value) {
            return Number(value);
        }
    }
});

var sliderValue = document.getElementById("slider1-span");

slider.noUiSlider.on("update", function(values, handle) {
    sliderValue.innerHTML = `${values[0]} - ${values[1]}`;
});

class DataCollector {

    getSelectedValues(selector, url) {
        const checkboxes = document.querySelectorAll(selector);
        const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);
        setUrl(url, selectedValues.join(','));

        return selectedValues;
    }

    getSalaryRangeValue() {
        const lowerValue = parseInt(document.querySelector('.noUi-handle-lower').getAttribute('aria-valuenow'));
        const upperValue = parseInt(document.querySelector('.noUi-handle-upper').getAttribute('aria-valuenow'));
        const salaryRangeList = lowerValue > minValue || upperValue < maxValue? [lowerValue, upperValue]: [];
        setUrl('salary-range', salaryRangeList.join(','));

        return salaryRangeList;
    };

    getSelectedSectorValue() {
        const selectedSectorBtn = document.querySelector('button[aria-selected="true"]');
        if (selectedSectorBtn) {
            const selectedSectorValue = selectedSectorBtn.innerText;
            setUrl('sector', selectedSectorValue);

            return selectedSectorValue;
        };

        return false;
    }

    collectData() {
        const data = {
            salary_range_lower: this.getSalaryRangeValue()[0],
            salary_range_upper: this.getSalaryRangeValue()[1],
            work_experiences: this.getSelectedValues(workExperiencesCheckboxes, 'work-experience'),
            employment_type: this.getSelectedValues(employmentTypeCheckboxes, 'employment-type'),
            work_preference: this.getSelectedValues(workPreferenceCheckboxes, 'work-preference'),
            department: this.getSelectedValues(departmentCheckboxes, 'department'),
            date_posted: this.getSelectedValues(datePostedRadios, 'date')[0],
            sector: this.getSelectedSectorValue()
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

    window.history.pushState('', '', decodeURIComponent(url));
};

const getUrlParameterValue = (parameterName) => {
    try {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const parameterValue = urlParams.get(parameterName);
        return parameterValue.split(',');

    } catch (error) {
        return [];
     };
};

const generatePagination = (paginationInfo) => {
    const container = document.getElementById('pagination-container');
    container.innerHTML = ''; // Clear existing content

    const currentPage = paginationInfo.current_page;
    const numPages = paginationInfo.num_pages;
    const hasPrevious = paginationInfo.has_previous;
    const hasNext = paginationInfo.has_next;
    const separator = url.searchParams.size ? '&':'?'; // return & or ? symbol

    url.hash = ''; // delete #job-list hash from url
    setUrl('page'); // delete page parameter from url

    // Previous button
    if (hasPrevious) {
        const previousItem = document.createElement('li');
        previousItem.className = 'page-item';
        previousItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${currentPage - 1}#job-list" tabindex="-1"><i class="mdi mdi-chevron-double-left fs-15"></i></a>`;
        container.appendChild(previousItem);
    };

    // Page numbers
    for (let i = 1; i <= numPages; i++) {
        if (i === 1 || i === numPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${i}#job-list">${i}</a>`;
            container.appendChild(pageItem);
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            const dotsItem = document.createElement('li');
            dotsItem.className = 'page-item';
            dotsItem.innerHTML = `<a class="page-link" href="${url}#job-list">...</a>`;
            container.appendChild(dotsItem);
        };
    };

    // Next button
    if (hasNext) {
        const nextItem = document.createElement('li');
        nextItem.className = 'page-item';
        nextItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${currentPage + 1}#job-list"><i class="mdi mdi-chevron-double-right fs-15"></i></a>`;
        container.appendChild(nextItem);
    };

};

const listVacancies = (vacanciesInfo, bookmarks, applications, keywords) => {
    const container = document.getElementById('job-list-container');
    container.innerHTML = ''; // Clear existing content

    for (const [key, vacancy] of Object.entries(vacanciesInfo)) {
        container.innerHTML += `
        <div id="vacancy-${vacancy.id}" class="job-box card mt-5 ${bookmarks.includes(vacancy.id) ? 'bookmark-post':''}">
            <div class="p-4">
                <div class="row">
                    <div class="col-lg-1">
                        <a href="/company/${vacancy.employer__username}"><img src="/static/main/images/featured-job/default-company-img.jpeg" alt="" class="img-fluid rounded-3"></a>
                    </div><!--end col-->
                    <div class="col-lg-10">
                        <div class="mt-3 mt-lg-0">
                            <h5 class="fs-17 mb-1"><a href="/vacancy/${vacancy.slug}" class="text-dark">${vacancy.position_title}</a> <small class="text-muted fw-normal">(${vacancy.work_experience_name})</small></h5>
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
                                <span class="badge bg-soft-success mt-1">Full Time</span>
                                <span class="badge bg-soft-warning mt-1">Urgent</span>
                                <span class="badge bg-soft-info mt-1">Private</span>
                            </div>
                        </div>
                    </div><!--end col-->
                </div><!--end row-->
                <div class="favorite-icon" style="cursor: pointer;" onclick="addBookmark(${vacancy.id})">
                    <a href="javascript:void(0);"><i class="uil uil-heart-alt fs-18"></i></a>
                </div>
            </div>
            <div class="p-3 bg-light">
                <div class="row justify-content-between">
                    <div class="col-md-8">
                    ${vacancy.keywords ? `
                        <div>
                            <ul class="list-inline mb-0">
                                <li class="list-inline-item"><i class="uil uil-tag"></i> Keywords :</li>
                                ${(() => {
                                    let itemsHtml = '';
                                    let lastItem = vacancy.keywords.slice(-1)[0];
                                    keywords.forEach(key => {
                                        if (vacancy.keywords.includes(String(key.id))){
                                            itemsHtml += `<li class="list-inline-item"><a href="javascript:void(0)" class="primary-link text-muted">${key.name}${key.id!=lastItem ? ',':''}</a></li>`;
                                        };
                                    });
                                    return itemsHtml;
                                })()}
                            </ul>
                        </div>
                    `:''}
                    </div>
                    <!--end col-->
                    <div class="col-md-3">
                        <div class="text-md-end">
                        ${(() => {
                            let applyId = `apply-now-${vacancy.id}`;
                            let applyText = 'Apply Now';

                            if (applications.includes(vacancy.id)) {
                                applyId = `delete-apply-${vacancy.id}`;
                                applyText = 'Delete Apply';
                            };

                            const apply = `<a href="javascript:void(0);" id="${applyId}" class="primary-link" onclick="apply(${vacancy.id})">${applyText} <i class="mdi mdi-chevron-double-right"></i></a>`;
                            return apply;
                        })()}
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
            generatePagination(
                response.pagination
            );

            listVacancies(
                response.vacancies,
                response.bookmarks,
                response.applications,
                response.keywords
            );
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

addCheckboxListener(workExperiencesCheckboxes, filterRequest); // Work Experiences Listener
addCheckboxListener(employmentTypeCheckboxes, filterRequest); // Type of Employment Listener
addCheckboxListener(workPreferenceCheckboxes, filterRequest); // Work Preference Listener
addCheckboxListener(departmentCheckboxes, filterRequest); // Department Listener
addCheckboxListener(datePostedRadios, filterRequest); // Date Posted Listener

// Set filter inputs from url parameters
slider.noUiSlider.set(getUrlParameterValue('salary-range'));
setFilterCheckboxes(workExperiencesCheckboxes, getUrlParameterValue('work-experience')); // Set work experience
setFilterCheckboxes(employmentTypeCheckboxes, getUrlParameterValue('employment-type')); // Set type of employment
setFilterCheckboxes(workPreferenceCheckboxes, getUrlParameterValue('work-preference')); // Set work preference
setFilterCheckboxes(departmentCheckboxes, getUrlParameterValue('department')); // Set work preference
setFilterCheckboxes(datePostedRadios, getUrlParameterValue('date')); // Set work preference


// Sector filter settings
const sectorsBtn = document.querySelectorAll('button[aria-selected="false"]');
const sectorUrlParam = getUrlParameterValue('sector');

sectorsBtn.forEach(btn => {
    if (btn.innerText == sectorUrlParam) {
        btn.setAttribute('aria-selected', true);
        btn.classList.add('active');
    };

    btn.addEventListener('click', filterRequest);
});


// Department items searcher
const departmentSearchInput = document.querySelector('#department input[type="search"]');
const departmentItems = document.querySelectorAll(departmentCheckboxes);

departmentSearchInput.addEventListener('input', function() {
    let searchValue = this.value.toLowerCase();

    Array.prototype.forEach.call(departmentItems, function(item) {
        let label = item.parentElement;

        if (label.textContent.toLowerCase().includes(searchValue)) {
            label.style.display = 'block';
        }else {
            label.style.display = 'none';
        }
    });
});