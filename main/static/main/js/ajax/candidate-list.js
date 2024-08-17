const citizenshipFilter = new Choices('#citizenship');
const jobFamilyFilter = new Choices('#job-family');
const choicesSingleFilterOrderby = new Choices('#choices-single-filter-orderby');
const choicesCandidatePage = new Choices('#choices-candidate-page');
const url = new URL(window.location);

const userInfoElement = document.getElementById('user-info');
const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated');
const signInModal = new bootstrap.Modal(document.getElementById('signinModal'));

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
                                    <a href="javascript:void(0)"><img src="${candidate.profile_photo ? candidate.profile_photo:'/static/main/images/user/default-profile.jpg'}" alt="${candidate.full_name}" class="avatar-md img-thumbnail rounded-circle"></a>
                            </div>
                        </div>
                        
                        <div class="col-lg-5 candidate-content">
                            <div class="candidate-list-content mt-3 mt-lg-0">
                                <h5 class="fs-19 mb-0"><a href="#" class="primary-link">${candidate.full_name}</a> <span class="badge bg-success ms-1"><i class="mdi mdi-star align-middle"></i> 4.8</span></h5>
                                <p class="text-muted mb-2"> Project Manager</p>
                                <ul class="list-inline mb-0 text-muted">
                                    <li class="list-inline-item">
                                        <i class="mdi mdi-map-marker"></i> Oakridge Lane Richardson
                                    </li>
                                    <li class="list-inline-item">
                                        <i class="uil uil-wallet"></i> $650 / hours
                                    </li>
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
            generatePagination(
                response.pagination
            );

            listCandidate(
                response.candidates
            );
        }

    });
};


jobFamilyFilter.passedElement.element.addEventListener('change', function(event) {
    setUrl('job-family', event.target.value);
    filterRequest();
});

citizenshipFilter.passedElement.element.addEventListener('change', function(event) {
    setUrl('citizenship', event.target.value);
    filterRequest();
});