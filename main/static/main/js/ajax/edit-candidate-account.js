const selects = document.querySelectorAll('select');
const educations = document.getElementById('educations');

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

const genHexString = () => {
    const hex = '456789ABCDEF';
    let output = '';
    for (let i = 0; i < 3; ++i) {
        output += hex.charAt(Math.floor(Math.random() * hex.length));
    }
    return output;
}

const deleteEducation = (button) => {
    const parentDiv = button.closest('.d-flex.justify-content-between');
    const education_id = parentDiv.id;
    parentDiv.remove();

    if (education_id) {
        $.ajax({
            url: '/ajax-delete-education',
            type: 'POST',
            data: {education_id: education_id},
        });
    };
};

const addEducation = () => {
    const randomId = genHexString();

    educations.insertAdjacentHTML('beforeend', `
    <div class="d-flex justify-content-between mb-5">
        <div class="w-100">
            <input type="hidden" name="education-id" value="">
            <div class="d-flex">
                <input name="school" type="text" class="form-control mb-2" placeholder="School">
                <button class="btn btn-danger fs-17 mb-2 ms-2" onclick="deleteEducation(this)"><i class="uil uil-trash-alt"></i></button>
            </div>
            <input name="speciality" type="text" class="form-control mb-2" placeholder="Speciality">
            <div class="d-flex mb-2">
                <input type="text" class="form-control" data-provide="datepicker" data-date-format="M, yyyy" id=""
                    name="start_date" placeholder="Started date">

                <input type="text" class="form-control ms-2" data-provide="datepicker" data-date-format="M, yyyy" id=""
                    name="end_date" placeholder="End date">
            </div>
            <textarea name="description" class="form-control" rows="3" placeholder="Description"></textarea>
        </div>
    </div>`);
};