const selects = document.querySelectorAll('select');
const educations = document.getElementById('educations');
const experiences = document.getElementById('experiences');
const projects = document.getElementById('projects');
const menus = document.querySelectorAll('.edit-menu');
const companiesCheckboxes = '#preference-companies input[type="checkbox"]';
const locationCheckboxes = '#preference-location input[type="checkbox"]';
const careerTypeCheckboxes = '#preference-career-type input[type="checkbox"]';
const typeOfEmploymentCheckboxes = '#preference-type-of-employment input[type="checkbox"]';

var tempPresentId = 26062001;

selects.forEach(select => {
    if (select.id == 'gender') {
        new Choices(`#${select.id}`, {
            searchEnabled: false,
            shouldSort: false,
            shouldSortItems: false, 
            fuseOptions: {
                includeScore: true,
                threshold: 0.2,
                location: 0,
                useExtendedSearch: true,
            }
        });
    }else {
        new Choices(`#${select.id}`, {
            searchResultLimit: 500,
            resetScrollPosition: false,
            shouldSort: false,
            shouldSortItems: false, 
            fuseOptions: {
                includeScore: true,
                threshold: 0.2,
                location: 0,
                useExtendedSearch: true,
            }
        });
    }
});

// Collects the values ​​selected from the Language selection into an input and prepares it for recording.
const languageSkils = document.getElementById('languages');
const languageValuesInput = document.getElementById('language-values');
const collectLanguageSkils = () => {
    let values = new Array();
    languageSkils.querySelectorAll('option').forEach((option) => {
        let value = option.value;
        if (value) {
            values.push(option.value);
        }
    });
    languageValuesInput.value = values;
};

if (languageSkils) {
    collectLanguageSkils();
    languageSkils.addEventListener('change', collectLanguageSkils);
}
// End

// Collects the values ​​selected from the Language selection into an input and prepares it for recording.
const functionalSkils = document.getElementById('functionals');
const functionalValuesInput = document.getElementById('functional-values');
const collectFunctionalSkils = () => {
    let values = new Array();
    functionalSkils.querySelectorAll('option').forEach((option) => {
        let value = option.value;
        if (value) {
            values.push(option.value);
        }
    });
    functionalValuesInput.value = values;
};

if (functionalSkils) {
    collectFunctionalSkils();
    functionalSkils.addEventListener('change', collectFunctionalSkils);
}
// End

const previewImg = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('profile-img').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    };
};


const getEducationPlaceholders = () => {
    const firstDiv = educations.querySelector('div');
    const school = firstDiv.querySelector("input[name='school']").placeholder;
    const speciality = firstDiv.querySelector("input[name='speciality']").placeholder;
    const startDate = firstDiv.querySelector("input[name='start_date']").placeholder;
    const endDate = firstDiv.querySelector("input[name='end_date']").placeholder;
    const description = firstDiv.querySelector("textarea[name='description']").placeholder;

    return {
        school: school,
        speciality: speciality,
        startDate: startDate,
        endDate: endDate,
        description: description
    }
    
};

const deleteEducation = (button) => {
    const directDivs = Array.from(educations.children).filter(el => el.tagName.toLowerCase() === 'div');

    if (directDivs.length > 1) {
        const parentDiv = button.closest('.d-flex.justify-content-between');
        const educationId = parentDiv.id;
        parentDiv.remove();

        if (educationId) {
            $.ajax({
                url: '/ajax/delete-education',
                type: 'POST',
                data: {education_id: educationId},
            });
        };
    };
};

const addEducation = () => {
    const index = educations.childElementCount;
    const placeholder = getEducationPlaceholders();

    educations.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="education_id" value="">
            <div class="d-flex">
                <input name="school" type="text" class="form-control mb-2" placeholder="${placeholder.school}" required>
                <button class="btn btn-danger fs-17 mb-2 ms-2" onclick="deleteEducation(this)"><i class="uil uil-trash-alt"></i></button>
            </div>

            <div class="d-flex mb-2">
                <div class="w-100 me-2">
                    <select class="form-select" data-trigger name="education_level" id="education-level-new-${index}" >
                        ${(() => {
                            let optionContainer = document.getElementById('option-container');
                            let options = optionContainer.querySelectorAll('option');
                            let optionList;
                            options.forEach(option => {
                                optionList += `<option value="${option.value}">${option.text}</option>`;
                            });

                            return optionList
                        })()}
                    </select>
                </div>
                <input name="speciality" type="text" class="form-control" placeholder="${placeholder.speciality}" required>
            </div>

            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy"
                    name="start_date" placeholder="${placeholder.startDate}" required>

                <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                    name="end_date" placeholder="${placeholder.endDate}" required>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="${placeholder.description}" required></textarea>
        </div>
    </div>`);

    new Choices(`#education-level-new-${index}`);
};

const getExperiencePlaceholders = () => {
    const firstDiv = experiences.querySelector('div');
    const companyName = firstDiv.querySelector("input[name='company_name']").placeholder;
    const title = firstDiv.querySelector("input[name='title']").placeholder;
    const startDate = firstDiv.querySelector("input[name='start_date']").placeholder;
    const endDate = firstDiv.querySelector("input[name='end_date']").placeholder;
    const present = firstDiv.querySelector(".form-check-label").textContent;
    const description = firstDiv.querySelector("textarea[name='description']").placeholder;

    return {
        companyName: companyName,
        title: title,
        startDate: startDate,
        endDate: endDate,
        present: present,
        description: description
    }
    
};

const deleteExperience = (button) => {
    const directDivs = Array.from(experiences.children).filter(el => el.tagName.toLowerCase() === 'div');
    if (directDivs.length > 1) {
        const parentDiv = button.closest('.d-flex.justify-content-between');
        const experienceId = parentDiv.id;
        parentDiv.remove();

        if (experienceId) {
            $.ajax({
                url: '/ajax/delete-experience',
                type: 'POST',
                data: {experience_id: experienceId},
            });
        };
    };
};

const addExperience = () => {
    const placeholder = getExperiencePlaceholders();

    experiences.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="experience_id" value="">
            <div class="d-flex">
                <input name="company_name" type="text" class="form-control mb-2" placeholder="${placeholder.companyName}" required>
                <button class="btn btn-danger fs-17 mb-2 ms-2" onclick="deleteExperience(this)"><i class="uil uil-trash-alt"></i></button>
            </div>
            <input name="title" type="text" class="form-control mb-2" placeholder="${placeholder.title}" required>
            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy"
                    name="start_date" placeholder="${placeholder.startDate}" required>

                <div class="input-group">
                    <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                        name="end_date" placeholder="${placeholder.endDate}" required>
                    <input type="hidden" name="end_date" value="" disabled="disabled">

                    <div class="input-group-append">
                        <div class="input-group-text">
                            <input type="hidden" name="present_id" value="${tempPresentId}">
                            <input class="form-check-input" type="checkbox" name="present-${tempPresentId}" id="present-t${tempPresentId}" onclick="endDateManage(this)">
                            <label class="form-check-label ms-2" for="present-t${tempPresentId}">${placeholder.present}</label>
                        </div>
                    </div>
                </div>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="${placeholder.description}"></textarea>
        </div>
    </div>`);

    tempPresentId += 12;
};

const getProjectPlaceholders = () => {
    const firstDiv = projects.querySelector('div');
    const companyName = firstDiv.querySelector("input[name='company_name']").placeholder;
    const title = firstDiv.querySelector("input[name='title']").placeholder;
    const startDate = firstDiv.querySelector("input[name='start_date']").placeholder;
    const endDate = firstDiv.querySelector("input[name='end_date']").placeholder;
    const present = firstDiv.querySelector(".form-check-label").textContent;
    const description = firstDiv.querySelector("textarea[name='description']").placeholder;
    const addGallery = firstDiv.querySelector("button[type='button']").innerHTML;

    return {
        companyName: companyName,
        title: title,
        startDate: startDate,
        endDate: endDate,
        present: present,
        description: description,
        addGallery: addGallery
    }
    
};

const deleteProject = (button) => {
    const directDivs = Array.from(projects.children).filter(el => el.tagName.toLowerCase() === 'div');
    if (directDivs.length > 1) {
        const parentDiv = button.closest('.d-flex.justify-content-between');
        const projectId = parentDiv.id;
        parentDiv.remove();

        if (projectId) {
            $.ajax({
                url: '/ajax/delete-project',
                type: 'POST',
                data: {project_id: projectId},
            });
        };
    };
};

const addProject = () => {
    const placeholder = getProjectPlaceholders();

    projects.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="project_id" value="">
            <div class="d-flex">
                <input name="company_name" type="text" class="form-control mb-2" placeholder="${placeholder.companyName}">
                <button class="btn btn-danger fs-17 mb-2 ms-2" onclick="deleteProject(this)"><i class="uil uil-trash-alt"></i></button>
            </div>
            <input name="title" type="text" class="form-control mb-2" placeholder="${placeholder.title}" required>
            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy"
                    name="start_date" placeholder="${placeholder.startDate}" required>

                <div class="input-group">
                    <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                        name="end_date" placeholder="${placeholder.endDate}" required>
                    <input type="hidden" name="end_date" value="" disabled="disabled">

                    <div class="input-group-append">
                        <div class="input-group-text">
                            <input type="hidden" name="present_id" value="${tempPresentId}">
                            <input class="form-check-input" type="checkbox" name="present-${tempPresentId}" id="present-t${tempPresentId}" onclick="endDateManage(this)">
                            <label class="form-check-label ms-2" for="present-t${tempPresentId}">${placeholder.present}</label>
                        </div>
                    </div>
                </div>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="${placeholder.description}"></textarea>
            <div class="project-gallery form-control mt-2">
                <div class="gallery-items"></div>
                <button class="btn btn-link add-gallery-btn" type="button">${placeholder.addGallery}</button>
                <input type="file" name="images-${tempPresentId}" class="image-input" style="display: none;" accept="image/*" multiple>
            </div>
        </div>
    </div>`);

    tempPresentId += 1;
};

const deleteProjectImage = (element, imageId) => {
    $.ajax({
        url: '/ajax/delete-project-image',
        type: 'POST',
        data: {image_id: imageId},
        success: () => {
            element.closest('.gallery-item').remove();
        }
    })
}

document.addEventListener('click', (event) => {
    if (event.target.closest('.add-gallery-btn')) {
        const galleryContainer = event.target.closest('.project-gallery');
        const imageInput = galleryContainer.querySelector('.image-input');
        imageInput.click();
    }
});

document.addEventListener('change', (event) => {
    if (event.target.matches('.image-input')) {
        const galleryContainer = event.target.closest('.project-gallery');
        const galleryItems = galleryContainer.querySelector('.gallery-items');
        const files = event.target.files;
        let itemLength = galleryItems.children.length;

        if (itemLength >= 5) {
            return;
        }

        Array.from(files).forEach((file, index) => {

            if (index >= 5 || itemLength+index >= 5) {
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                // Create gallery item
                const galleryItem = document.createElement('div');
                galleryItem.className = 'gallery-item';

                // Add image
                const img = document.createElement('img');
                img.src = e.target.result;
                galleryItem.appendChild(img);

                // Add remove button
                const removeBtn = document.createElement('span');
                removeBtn.className = 'remove-btn';
                removeBtn.innerText = 'x';
                removeBtn.addEventListener('click', () => {
                    galleryItems.removeChild(galleryItem);
                });
                galleryItem.appendChild(removeBtn);

                // Add to gallery
                galleryItems.appendChild(galleryItem);
            };
            reader.readAsDataURL(file);
        });
    }
});


const endDateManage = (input) => {
    const endDateInputText = input.closest('div.input-group').querySelector("input[name='end_date'][type='text']");
    const endDateInputHidden = input.closest('div.input-group').querySelector("input[name='end_date'][type='hidden']");

    if (input.checked) {
        endDateInputText.setAttribute('disabled', 'disabled');
        endDateInputText.removeAttribute('required');
        endDateInputHidden.removeAttribute('disabled');
    }else {
        endDateInputText.removeAttribute('disabled');
        endDateInputText.setAttribute('required', true),
        endDateInputHidden.setAttribute('disabled', 'disabled');
    };
};

const toggleMenu = (menuId) => {
    var menu = document.getElementById(menuId);
    var isMenuVisible = menu.style.display === 'block';
    closeAllMenus();
    if (!isMenuVisible) {
        menu.style.display = 'block';
    }
};

const closeAllMenus = () => {
    menus.forEach(function(menu) {
        menu.style.display = 'none';
    });
};

const removeImage = (imageId) => {
    var img = document.getElementById(imageId);

    $.ajax({
        url: '/ajax/delete-profile-image',
        type: 'POST',
        data: {image_id: imageId},
        success: function () {
            img.src = '/static/main/images/featured-job/default-company-img.jpeg';
        }
    });
};

document.addEventListener('click', function(event) {
    var isClickInsideMenu = event.target.closest('.profile-photo-edit') || event.target.closest('.edit-menu');
    if (!isClickInsideMenu) {
        closeAllMenus();
    }
});

const itemSearcher = (searchInput, items) => {
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            let searchValue = this.value.toLowerCase();
        
            Array.prototype.forEach.call(items, function(item) {
                const label = item.parentElement;
        
                if (label.textContent.toLowerCase().includes(searchValue)) {
                    label.style.display = 'block';
                }else {
                    label.style.display = 'none';
                }
            });
        });
    }
}

// Companies items searcher
const companiesSearchInput = document.querySelector('#preference-companies input[type="search"]');
const companiesItems = document.querySelectorAll(companiesCheckboxes);
itemSearcher(companiesSearchInput, companiesItems);

// Type of Employment items searcher
const locationSearchInput = document.querySelector('#preference-location input[type="search"]');
const locationItems = document.querySelectorAll(locationCheckboxes);
itemSearcher(locationSearchInput, locationItems);

const savePreference = () => {
    let selectedCompanies = Array.from(document.querySelectorAll(`${companiesCheckboxes}:checked`)).map(checkbox => checkbox.value);
    let selectedLocations = Array.from(document.querySelectorAll(`${locationCheckboxes}:checked`)).map(checkbox => checkbox.value);
    let selectedCareerTypes = Array.from(document.querySelectorAll(`${careerTypeCheckboxes}:checked`)).map(checkbox => checkbox.value);
    let selectedTypesOfEmployment = Array.from(document.querySelectorAll(`${typeOfEmploymentCheckboxes}:checked`)).map(checkbox => checkbox.value);
    let minimumSalary = document.getElementById('preference-minimum-salary').value ;
    let maximumSalary = document.getElementById('preference-maximum-salary').value;

    let dataJson = {
        companies: JSON.stringify(selectedCompanies),
        locations: JSON.stringify(selectedLocations),
        career_types: JSON.stringify(selectedCareerTypes),
        types_of_employment: JSON.stringify(selectedTypesOfEmployment),
        minimum_salary: minimumSalary,
        maximum_salary: maximumSalary
    }

    $.ajax({
        url: '/ajax/manage-candidate-preference',
        type: 'POST',
        data: dataJson,
        success: () => {
            window.location.reload()
        }
    });
}


// Tab settings
const url = new URL(window.location);
const tabButtons = document.querySelectorAll('[data-bs-toggle="pill"]');
const nextUrl = document.querySelectorAll('input[name="next"]');

tabButtons.forEach(button => {
    button.addEventListener('shown.bs.tab', (event) => {
        const targetTabId = event.target.getAttribute('data-bs-target').replace('#', '');
        updateUrlParameter('tab', targetTabId);
        updateNextInputs();
    });
});

const urlParams = new URLSearchParams(window.location.search);
const tabParam = urlParams.get('tab');
if (tabParam) {
    const targetTab = document.querySelector(`[data-bs-target="#${tabParam}"]`);
    if (targetTab) {
        const bootstrapTab = new bootstrap.Tab(targetTab);
        bootstrapTab.show();
    }
};

const updateUrlParameter = (param, value) => {
    if (value) {
        url.searchParams.set(param, value);
    } else {
        url.searchParams.delete(param);
    }
    window.history.replaceState({}, '', url);
};

const updateNextInputs = () => {
    nextUrl.forEach(input => {
        input.value = url.href;
    });
};

// WhatsApp Input
const whatsappNumber = document.getElementById('whatsapp_number');
if (whatsappNumber) {
    whatsappNumber.addEventListener('input', function (e) {
        const allowedChars = /^[0-9+]*$/;
    
        if (!allowedChars.test(this.value)) {
            this.value = this.value.replace(/[^0-9+]/g, '');
        }
    });
};

// Employer Review Settings
const deleteReviewModal = new bootstrap.Modal(document.getElementById('deleteReviewModal'));
const deleteReviewBtn = document.getElementById('delete-review-btn');

$('#deleteReviewModal').on('hidden.bs.modal', function(e) {
    deleteReviewBtn.removeAttribute('onclick');
});

const deleteRequest = (id) => {
    deleteReviewBtn.setAttribute('onclick', `deleteReview(${id})`);
    deleteReviewModal.show();
};

const deleteReview = (id) => {
    $.ajax({
        url:'/ajax/delete-review',
        type: 'POST',
        data: {review_id: id},
        success: (response) => {
            if (response.success) {
                document.getElementById(`review-${id}`).remove();
            }
            deleteReviewModal.hide();
        }
    });
};

const sendReviewBtn = document.getElementById('submit-review-btn');
const editReviewBtn = document.getElementById('edit-review-btn');
const reviewInput = document.getElementById('review-input');
const textarea = document.getElementById('review-input');
const charCounter = document.getElementById('char-counter');
const minLength = 190;
const maxLength = 950;

const checkChartCount = () => {
    const charCount = textarea.value.length;
    charCounter.innerText = `${charCount}`;

    if (charCount < minLength || charCount > maxLength) {
        charCounter.style.setProperty('color', '#da3746', 'important');
    } else {
        charCounter.style.color = '#adb5bd';
    }
}

textarea.addEventListener('input', () => {
    checkChartCount();
});

document.getElementById('submit-review-btn').addEventListener('click', (event) => {
    const charCount = textarea.value.length;
    if (charCount > minLength && charCount < maxLength) {
        event.target.closest('form').submit();
    }
})

const editReview = (id) => {
    let reviewText = document.getElementById(`review-text-${id}`).innerText;
    reviewInput.value = reviewText;

    sendReviewBtn.style.display = 'none';
    editReviewBtn.style.display = 'inline';

    editReviewBtn.setAttribute('onclick', `editRequest('${id}')`);
    checkChartCount();
}

const editRequest = (id) => {
    const charCount = textarea.value.length;

    if (charCount > minLength && charCount < maxLength) {
        $.ajax({
            url: '/ajax/edit-review',
            type: 'POST',
            data: {
                review_id: id,
                new_review: reviewInput.value
            },
            success: (response) => {
                if (response.success) {
                    let reviewText = document.getElementById(`review-text-${id}`);
                    reviewText.innerText = response.new_review;
                }
    
                reviewInput.value = '';
                sendReviewBtn.style.display = 'inline';
                editReviewBtn.style.display = 'none';
                editReviewBtn.removeAttribute('onclick');
                checkChartCount();
            }
        })
    }
}

const manageReviewVisibility = (id, visibility) => {
    const makeVisibleBtn = document.getElementById(`make-review-visible-${id}`);
    const makeInvisibleBtn = document.getElementById(`make-review-invisible-${id}`);
    const visibilityStatus = document.getElementById(`visibility-status-${id}`);

    $.ajax({
        url: '/ajax/manage-review-visibility',
        type: 'POST',
        data: {
            review_id: id,
            visibility: visibility
        },
        success: (response) => {
            if (response.visibility) {
                makeVisibleBtn.style.display = 'none';
                makeInvisibleBtn.style.display = 'block';
                visibilityStatus.style.display = 'none';
            } else {
                makeVisibleBtn.style.display = 'block';
                makeInvisibleBtn.style.display = 'none';
                visibilityStatus.style.display = 'inline';
            };
        }
    })
}