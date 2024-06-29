const candidateActionModal = new bootstrap.Modal(document.getElementById('candidateAction'));

const applicantMessage = document.getElementById('applicant-message');

const actions = document.getElementById("action");
const requestOtherDateInput = document.getElementById('request-other-date');
const theme = localStorage.getItem('theme');
const darkThemeLink = document.getElementById('flatpickr-dark');
const modalTitle = document.getElementById('modal-title');
const requestOtherDateInfoText = document.getElementById('request-other-date-info-text')
const sendActionBtn = document.getElementById('send-action-btn');

const singleFilterChoices = new Choices('#choices-single-filter-orderby');
const singleCandidate=new Choices("#choices-candidate-page");
const actionChoices = new Choices('#action', {
    shouldSort: false,
    shouldSortItems: false,
    searchEnabled: false
});

flatpickr(requestOtherDateInput, {
    enableTime: true,
    dateFormat: "d-m-Y H:i",
    time_24hr: true,
    disableMobile: true
});


if (theme == 'dark') {
    darkThemeLink.disabled = false;
} else {
    darkThemeLink.disabled = true;
};

actions.addEventListener('change', function() {
    if (actions.value == 'REQUEST_OTHER_DATE') {
        requestOtherDateInput.closest('div').style.display = 'inline';
        requestOtherDateInfoText.style.display = 'inline';
    } else {
        requestOtherDateInput.closest('div').style.display = 'none';
        requestOtherDateInfoText.style.display = 'none';
    };
});

requestOtherDateInput.addEventListener('change', function () {
    requestOtherDateInput.style.borderColor = '';
});

$('#candidateAction').on('hidden.bs.modal', function (e) {
    modalTitle.innerText = '';
    requestOtherDateInput.value = '';
    requestOtherDateInput.style.borderColor = '';
    requestOtherDateInput.closest('div').style.display = 'none';
    requestOtherDateInfoText.style.display = 'none';
    actionChoices.setChoiceByValue('ACCEPT');
    sendActionBtn.removeAttribute('onclick');
});

const action = (id) => {
    const hasValueAction = document.getElementById(`has-value-action-${id}`).value;
    const hasValueRequestOtherDate = document.getElementById(`has-value-request-other-date-${id}`).value;

    if (hasValueAction) {
        actionChoices.setChoiceByValue(hasValueAction);
    };

    if (hasValueAction == 'REQUEST_OTHER_DATE') {
        requestOtherDateInput.closest('div').style.display = 'inline';
        requestOtherDateInput.value = hasValueRequestOtherDate;
    };

    const vacancyName = document.getElementById(`vacancy-name-${id}`).innerText;
    modalTitle.innerText = vacancyName;
    sendActionBtn.setAttribute('onclick', `sendAction(${id})`);
    candidateActionModal.show();
};

const sendAction = (id) => {
    const selectedActionValue = document.getElementById('action').value;
    const selectedRequestOtherDate = document.getElementById('request-other-date').value;

    if (selectedActionValue == 'REQUEST_OTHER_DATE' && selectedRequestOtherDate == '') {
        requestOtherDateInput.style.borderColor = '#DA3746';
        return;
    };

    $.ajax({
        url: '/ajax/send-candidate-action',
        type: 'POST',
        data: {
            applicant_id: id,
            action_value: selectedActionValue,
            request_other_date: selectedRequestOtherDate
        },
        success: function() {
            candidateActionModal.hide();
            const asctionStatus = document.getElementById(`action-status-${id}`);
            document.getElementById(`has-value-action-${id}`).value = selectedActionValue;
            document.getElementById(`has-value-request-other-date-${id}`).value = selectedRequestOtherDate;
            
            if (selectedActionValue == 'ACCEPT') {
                asctionStatus.innerHTML = 'Accepted <i class="uil uil-check-circle">';
                asctionStatus.classList = 'btn btn-primary';

            } else if (selectedActionValue == 'REJECT') {
                asctionStatus.innerHTML = 'Rejected <i class="uil uil-times-circle">';
                asctionStatus.classList = 'btn btn-danger';

            } else if (selectedActionValue == 'REQUEST_OTHER_DATE') {
                asctionStatus.innerHTML = `<span>Requested Date<br>${selectedRequestOtherDate}</span> <i class="uil uil-clock-eight"></i>`;
                asctionStatus.classList = 'btn btn-success';
            };
        }
    });
};