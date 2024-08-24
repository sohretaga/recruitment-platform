const selects = document.querySelectorAll('select');
const educations = document.getElementById('educations');
const experiences = document.getElementById('experiences');
const menus = document.querySelectorAll('.edit-menu');
const companiesCheckboxes = '#preference-companies input[type="checkbox"]';
const locationCheckboxes = '#preference-location input[type="checkbox"]';

var tempPresentId = 1;

selects.forEach(select => {
    new Choices(`#${select.id}`);
});


// Collects the values ​​selected from the Language selection into an input and prepares it for recording.
const languageSkils = document.getElementById('languages');
const languageValuesInput = document.getElementById('langauge-values');
languageSkils.addEventListener('change', function() {
    let values = new Array();
    languageSkils.querySelectorAll('option').forEach((option) => {
        values.push(option.value);
    });
    languageValuesInput.value = values;
});
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

const deleteEducation = (button) => {
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

const addEducation = () => {
    let index = educations.childElementCount

    educations.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="education_id" value="">
            <div class="d-flex">
                <input name="school" type="text" class="form-control mb-2" placeholder="School*" required>
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
                <input name="speciality" type="text" class="form-control" placeholder="Speciality*" required>
            </div>

            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy"
                    name="start_date" placeholder="Start date*" required>

                <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                    name="end_date" placeholder="End date*" required>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="Description*" required></textarea>
        </div>
    </div>`);

    new Choices(`#education-level-new-${index}`);
};

const deleteExperience = (button) => {
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

const addExperience = () => {
    experiences.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="experience_id" value="">
            <div class="d-flex">
                <input name="company_name" type="text" class="form-control mb-2" placeholder="Company name*" required>
                <button class="btn btn-danger fs-17 mb-2 ms-2" onclick="deleteExperience(this)"><i class="uil uil-trash-alt"></i></button>
            </div>
            <input name="title" type="text" class="form-control mb-2" placeholder="Title*" required>
            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy"
                    name="start_date" placeholder="Start date*" required>

                <div class="input-group">
                    <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                        name="end_date" placeholder="End date" required>
                    <input type="hidden" name="end_date" value="" disabled="disabled">

                    <div class="input-group-append">
                        <div class="input-group-text">
                            <input type="hidden" name="present_id" value="${tempPresentId}">
                            <input class="form-check-input" type="checkbox" name="present-${tempPresentId}" id="present-t${tempPresentId}" onclick="endDateManage(this)">
                            <label class="form-check-label ms-2" for="present-t${tempPresentId}">Present</label>
                        </div>
                    </div>
                </div>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="Description*"></textarea>
        </div>
    </div>`);

    tempPresentId += 1;
};

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

// Companies items searcher
const companiesSearchInput = document.querySelector('#preference-companies input[type="search"]');
const companiesItems = document.querySelectorAll(companiesCheckboxes);
itemSearcher(companiesSearchInput, companiesItems);

// Type of Employment items searcher
const locationSearchInput = document.querySelector('#preference-location input[type="search"]');
const locationItems = document.querySelectorAll(locationCheckboxes);
itemSearcher(locationSearchInput, locationItems);