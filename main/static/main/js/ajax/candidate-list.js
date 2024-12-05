const candidateCount = document.getElementById('candidate-count');
const url = new URL(window.location);

const userInfoElement = document.getElementById('user-info');
const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated');
const signInModal = new bootstrap.Modal(document.getElementById('signinModal'));

const citizenshipCheckboxes = '#citizenship input[type="checkbox"]';
const ageGroypCheckboxes = '#age-group input[type="checkbox"]';
const genderCheckboxes = '#gender input[type="checkbox"]';
const workExperienceCheckboxes = '#work-experience input[type="checkbox"]';
const educationLevelCheckboxes = '#education-level input[type="checkbox"]';

const vacancyFilterBtn = document.getElementById('vacancy-filter');
const clearVacancyFilterBtn = document.getElementById('clear-vacancy-filter');

const filterOrderby = new Choices('#choices-single-filter-orderby', {
    shouldSort: false,
    shouldSortItems: false,
    searchEnabled: false,
});
const candidatePage = new Choices('#choices-candidate-page', {
    shouldSort: false,
    shouldSortItems: false,
    searchEnabled: false,
});
const jobFamily = new Choices('#job-family');

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

const addCandidateBookmark = (id) => {

    if (isAuthenticated == 'yes'){
        const candidateBox = document.getElementById(`candidate-${id}`);

        if (candidateBox.classList.contains('bookmark-post')) {
            candidateBox.classList.remove('bookmark-post');
        }else {
            candidateBox.classList.add('bookmark-post');
        }
    
        $.ajax({
            url: '/ajax/add-candidate-bookmark',
            type: 'POST',
            data: {
                candidate: id,
            }
        });

    }else {
        signInModal.show();
    }
};

const generatePagination = (paginationInfo) => {
    const container = document.getElementById('pagination-container');
    container.innerHTML = ''; // Clear existing content

    const currentPage = paginationInfo.current_page;
    const numPages = paginationInfo.num_pages;
    const hasPrevious = paginationInfo.has_previous;
    const hasNext = paginationInfo.has_next;
    const separator = url.searchParams.size ? '&':'?'; // return & or ? symbol

    // url.hash = ''; // delete #job-list hash from url
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

const listCandidate = (candidateInfo) => {
    const container = document.getElementById('candidate-container');
    container.innerHTML = ''; // Clear existing content

    for (const [key, candidate] of Object.entries(candidateInfo)) {
        container.innerHTML += `
            <div id="candidate-${candidate.id}" class="candidate-list-box card mt-4  ${candidate.is_bookmark ? 'bookmark-post':''}">
                <div class="card-body p-4">
                    <div class="row align-items-center candidate-row">
                        <div class="col-auto">
                            <div class="candidate-list-images">
                                    <a href="/candidate/${candidate.username}"><img src="${candidate.profile_photo ? candidate.profile_photo:'/static/main/images/user/default-profile.jpg'}" alt="${candidate.full_name}" class="avatar-md img-thumbnail rounded-circle"></a>
                            </div>
                        </div>
                        
                        <div class="col-lg-5 candidate-content">
                            <div class="candidate-list-content mt-3 mt-lg-0">
                                <h5 class="fs-19 mb-0"><a href="/candidate/${candidate.username}" class="primary-link">${candidate.full_name}</a> <span class="badge bg-success ms-1"><i class="mdi mdi-star align-middle"></i> 4.8</span></h5>
                                <p class="text-muted mb-2"> ${candidate.occupation_name ? candidate.occupation_name:''}</p>
                                <ul class="list-inline mb-0 text-muted">
                                    ${(() => {
                                        if (candidate.citizenship_name) {
                                            return `<li class="list-inline-item">
                                                <i class="mdi mdi-map-marker"></i> ${candidate.citizenship_name}
                                            </li>`
                                        }else {return ''}
                                    })()}

                                    ${(() => {
                                        if (candidate.offered_salary) {
                                            return `<li class="list-inline-item">
                                                <i class="uil uil-wallet"></i> ${candidate.offered_salary} AZN
                                            </li>`
                                        }else {return ''}
                                    })()}
                                </ul>
                            </div>
                        </div>

                        <div class="col-lg-4">
                            <div class="mt-2 mt-lg-0">
                                <span class="badge bg-soft-muted fs-14 mt-1">Leader</span> <span class="badge bg-soft-muted fs-14 mt-1">Manager</span>
                                <span class="badge bg-soft-muted fs-14 mt-1">Developer</span>
                            </div>
                        </div>
                    </div>
                    <div class="favorite-icon" onclick="addCandidateBookmark('${candidate.id}')">
                        <a href="javascript:void(0)"><i class="uil uil-heart-alt fs-18"></i></a>
                    </div>
                </div>
            </div>`
    };
};

// Filter Request
const filterRequest = () => {
    const params = new URLSearchParams(url.search)
    const jsonData = {};
    params.forEach((value, key) => {
        jsonData[key] = value
    });

    $.ajax({
        url: '/ajax/filter-candidate',
        type: 'POST',
        data: jsonData,
        success: (response) => {
            candidateCount.innerText = response.candidate_count;
            generatePagination(
                response.pagination
            );

            listCandidate(
                response.candidates
            );
        }

    });
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

const setUrlWithSelectedCheckboxes = (selector, query_key) => {
    const checkboxes = document.querySelectorAll(selector);
    const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
    const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);
    setUrl(query_key, selectedValues.join(','));
}

const addCheckboxListener = (selector, query_key, callback) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            setUrlWithSelectedCheckboxes(selector, query_key);
            callback();
        });
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

addCheckboxListener(citizenshipCheckboxes, 'citizenship', filterRequest); // Citizenship Listener
addCheckboxListener(ageGroypCheckboxes, 'age-group', filterRequest); // Age Group Listener
addCheckboxListener(genderCheckboxes, 'gender', filterRequest); // Gender Listener
addCheckboxListener(workExperienceCheckboxes, 'work-experience', filterRequest); // Work Experience Listener
addCheckboxListener(educationLevelCheckboxes, 'education-level', filterRequest); // Education Level Listener

// Set filter inputs from url parameters
setFilterCheckboxes(citizenshipCheckboxes, getUrlParameterValue('citizenship')); // Set citizenship
setFilterCheckboxes(ageGroypCheckboxes, getUrlParameterValue('age-group')); // Set age group
setFilterCheckboxes(genderCheckboxes, getUrlParameterValue('gender')); // Set gender
setFilterCheckboxes(workExperienceCheckboxes, getUrlParameterValue('work-experience')); // Set work experience
setFilterCheckboxes(educationLevelCheckboxes, getUrlParameterValue('education-level')); // Set education level

// Citizenship items searcher
const citizenshipSearchInput = document.querySelector('#citizenship input[type="search"]');
const citizenshipItems = document.querySelectorAll(citizenshipCheckboxes);

citizenshipSearchInput.addEventListener('input', function() {
    let searchValue = this.value.toLowerCase();

    Array.prototype.forEach.call(citizenshipItems, function(item) {
        const label = item.parentElement;

        if (label.textContent.toLowerCase().includes(searchValue)) {
            label.style.display = 'block';
        }else {
            label.style.display = 'none';
        }
    });
});

// Clear Filter
const setFilterBtn = (clear) => {
    if (clear) {
        vacancyFilterBtn.style.display = 'none';
        clearVacancyFilterBtn.style.display = 'inline-block';
    }else {
        vacancyFilterBtn.style.display = 'inline-block';
        clearVacancyFilterBtn.style.display = 'none';
    }
};

const unselectAllFilters = (selector) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        if (checkbox.value) {
            checkbox.checked = false;
        }
    });
};

const clearFilter = () => {
    setUrl('citizenship');
    setUrl('age-group');
    setUrl('gender');
    setUrl('work-experience');
    setUrl('education-level');

    unselectAllFilters(citizenshipCheckboxes);
    unselectAllFilters(ageGroypCheckboxes);
    unselectAllFilters(genderCheckboxes);
    unselectAllFilters(workExperienceCheckboxes);
    unselectAllFilters(educationLevelCheckboxes);

    filterRequest();
};

const observer = new MutationObserver(() => {
    const params = new URLSearchParams(window.location.search);
    const allParams = [
        params.get('citizenship'),
        params.get('age-group'),
        params.get('gender'),
        params.get('work-experience'),
        params.get('education-level')
    ];

    if (allParams.some(param => param)) {
        setFilterBtn(clear=true);
    } else {
        setFilterBtn(clear=false);
    };
});

observer.observe(document, { subtree: true, childList: true });