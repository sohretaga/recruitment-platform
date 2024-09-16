var targetNode = document.querySelector('li.next a');
var nextBtn = document.querySelector('li.next');
var previousBtn = document.querySelector('li.previous a');
var config = { attributes: true, attributeFilter: ['class'] };
var selectedJobTitleId = '';

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrf_token);
        $('body').css('cursor', 'wait');
    },
    complete: function () {
        $('body').css('cursor', 'default');
    },
    error: function () {
        console.error('Failure when operation performed...');
    }
});

// Select2 Config
(function(i) {
    "use strict";

    function a() {}

    a.prototype.init = function() {
        i(".select2").select2();
        
        // Set seleceted values
        var selectedValues = i("#keywordsInput").val().replace(/'/g, '"');
        if (selectedValues){
            i("#keywordsSelect").val(JSON.parse(selectedValues)).trigger('change');
            i("#keywordsInput").val(JSON.stringify(selectedValues));
        };

        // Update hidden input on change
        i("#keywordsSelect").on('change', function() {
            var selectedValues = i(this).val();
            i("#keywordsInput").val(`"[${selectedValues}]"`);
        });
    };

    i.AdvancedForm = new a;
    i.AdvancedForm.Constructor = a;

    // Gets the value selected in the Job Title field
    selectedJobTitleId = $('#job-title').val();
    $('#job-title').on('select2:select', function(e) {
        selectedJobTitleId = $(this).val();
        autoFetchDefinition();
    });
})(window.jQuery);

(function() {
    "use strict";
    window.jQuery.AdvancedForm.init();
})();

const fetchDefinition = (requestedField) => {
    if (selectedJobTitleId) {
        $.ajax({
            url: '/dashboard/ajax/fetch-definition',
            type: 'POST',
            data: {
                requested_field: requestedField,
                job_title_id: selectedJobTitleId
            },
            success: (response) => {
                const definition = response.definition;
                const editor = window[requestedField]
                editor.setData(definition);
            }
        })
    }
};

const autoFetchDefinition = () => {
    if (selectedJobTitleId) {
        $.ajax({
            url: '/dashboard/ajax/auto-fetch-definition',
            type: 'POST',
            data: {
                job_title_id: selectedJobTitleId
            },
            success: (response) => {
                let descriptionData = response.description;
                let responsibilitiesData = response.responsibilities
                let qualificationData = response.qualification;
                let skillExperienceData = response.skill_experience;

                if (descriptionData) {
                    if (!description.getData()) {
                        description.setData(descriptionData);
                    }
                }

                if (responsibilitiesData) {
                    if (!responsibilities.getData()) {
                        responsibilities.setData(responsibilitiesData);
                    }
                }

                if (qualificationData) {
                    if (!qualification.getData()) {
                        qualification.setData(qualificationData);
                    }
                }

                if (skillExperienceData) {
                    if (!skill_experience.getData()) {
                        skill_experience.setData(skillExperienceData);
                    }
                }
            }
        })
    }
};

const confirmBtn = document.querySelector('#confirm-detail button');
confirmBtn.addEventListener('click', () => {
    let positionTitle = document.querySelector("input[name='position_title']").value;
    let salaryMaximum = document.querySelector("input[name='salary_maximum']").value;
    let salaryMinimum = document.querySelector("input[name='salary_minimum']").value;
    let salary = document.querySelector("input[name='salary']").value;

    if (positionTitle && salaryMaximum && salaryMinimum && salary) {
        document.getElementById('post-vacancy').submit();
    }else {
        $('.bs-confirm-detail-modal').modal('show')
    }
});