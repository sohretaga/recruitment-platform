let selectTags = document.querySelectorAll('select');
let inputTags = document.querySelectorAll('input');
let vacanciesDiv = document.getElementById('vacancies');

function getSelectedValues() {
    var selectedValues = [];
    var inputs = document.querySelectorAll('#employee-type-filters input[type="checkbox"]');

    inputs.forEach(function(input) {
        if(input.checked) {
            selectedValues.push(input.value);
        }
    });

    return selectedValues;
}

function loadData() {
    let career_type = document.getElementById('career_type').value;
    let career_level = document.getElementById('career_level').value;
    let location = document.getElementById('location').value;
    let fte = document.getElementById('fte').value;
    let employee_type  = JSON.stringify(getSelectedValues());

    $.ajax({
        data: {
            'employee_type': employee_type,
            'career_type': career_type,
            'career_level': career_level,
            'location': location,
            'fte': fte,
        },
        type: 'POST',
        url: loadUrl,
            success: function (response) {
                vacanciesDiv.innerHTML = '';
                vacancies = JSON.parse(response.vacancies);

                Array.prototype.forEach.call(vacancies, function(vacancy){
                    fields = vacancy.fields;
                    vacanciesDiv.innerHTML += `
                    <div class="col-md-6 col-lg-12">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title">${fields.name}</h3>
                            </div>
                            <div class="panel-body">
                                <p><strong>Location:</strong>${fields.location}</p>
                                <p><strong>Salary:</strong> $2500 - $3500 / pm</p>
                                <p><strong>Type:</strong>${fields.fte}</p>
                                <a href="#" class="btn btn-primary">Apply Now</a>
                            </div>
                        </div>
                    </div>
                    `
                })
            },
            error: function (response) {
                console.log(response.responseJSON.errors)
            }
        });
}


Array.prototype.forEach.call(selectTags, function(tag){
    tag.addEventListener('change', function(){
        loadData()
    })
});

Array.prototype.forEach.call(inputTags, function(tag){
    tag.addEventListener('change', function(){
        loadData()
    })
});


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});