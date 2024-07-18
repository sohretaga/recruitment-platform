const selects = document.querySelectorAll('select');
const educations = document.getElementById('educations');
const experiences = document.getElementById('experiences')
var tempPresentId = 1;

selects.forEach(select => {
    new Choices(`#${select.id}`)
});


// Collects the values ​​selected from the Language selection into an input and prepares it for recording.
const languages = document.getElementById('languages');
const languageValuesInput = document.getElementById('langauge-values');
languages.addEventListener('change', function() {
    let values = new Array();
    languages.querySelectorAll('option').forEach((option) => {
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
    const education_id = parentDiv.id;
    parentDiv.remove();

    if (education_id) {
        $.ajax({
            url: '/ajax/delete-education',
            type: 'POST',
            data: {education_id: education_id},
        });
    };
};

const addEducation = () => {
    educations.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="education_id" value="">
            <div class="d-flex">
                <input name="school" type="text" class="form-control mb-2" placeholder="School*" required>
                <button class="btn btn-danger fs-17 mb-2 ms-2" onclick="deleteEducation(this)"><i class="uil uil-trash-alt"></i></button>
            </div>
            <input name="speciality" type="text" class="form-control mb-2" placeholder="Speciality*" required>
            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy"
                    name="start_date" placeholder="Start date*" required>

                <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                    name="end_date" placeholder="End date*" required>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="Description*" required></textarea>
        </div>
    </div>`);
};


const deleteExperience = (button) => {
    const parentDiv = button.closest('.d-flex.justify-content-between');
    const experience_id = parentDiv.id;
    parentDiv.remove();

    if (experience_id) {
        $.ajax({
            url: '/ajax/delete-experience',
            type: 'POST',
            data: {experience_id: experience_id},
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

                <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy"
                    name="end_date" placeholder="End date*" required>
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="Description*"></textarea>
            <div class="form-check mt-2">
                <input class="form-check-input" type="checkbox" name="present" id="present-t${tempPresentId}">
                <label class="form-check-label" for="present-t${tempPresentId}">Present</label>
            </div>
        </div>
    </div>`);

    tempPresentId += 1;
};