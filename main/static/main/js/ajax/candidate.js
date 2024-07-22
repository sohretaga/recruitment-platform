const candidateActionModal = new bootstrap.Modal(document.getElementById('candidateAction'));
const deleteApplicationModal = new bootstrap.Modal(document.getElementById('deleteApplicationModal'));

const deleteApplicationBtn = document.getElementById('delete-application-btn');
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
    const hasValueEmployerAction = document.getElementById(`has-value-employer-action-${id}`);

    if (hasValueAction && hasValueEmployerAction != 'SUGGEST_OTHER_DATE') {
        actionChoices.setChoiceByValue(hasValueAction);
    }else {
        actionChoices.setChoiceByValue('ACCEPT');
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
            const hasValueInviteDate = document.getElementById(`has-value-invite-date-${id}`);
            document.getElementById(`has-value-action-${id}`).value = selectedActionValue;
            document.getElementById(`has-value-request-other-date-${id}`).value = selectedRequestOtherDate;  
            const employerId = document.getElementById(`employer-user-${id}`).value;
            
            if (selectedActionValue == 'ACCEPT') {
                asctionStatus.innerHTML = `<span>Invitation Accepted<br>${hasValueInviteDate.value}</span> <i class="uil uil-check-circle">`;
                asctionStatus.classList = 'btn btn-primary';

            } else if (selectedActionValue == 'REJECT') {
                asctionStatus.innerHTML = `<span>Rejected Invitation<br>${hasValueInviteDate.value}</span> <i class="uil uil-times-circle"></i>`;
                asctionStatus.classList = 'btn btn-danger';

            } else if (selectedActionValue == 'REQUEST_OTHER_DATE') {
                asctionStatus.innerHTML = `<span>Requested Another Date<br>${selectedRequestOtherDate}</span> <i class="uil uil-clock-eight"></i>`;
                asctionStatus.classList = 'btn btn-success';
            };

            sendNotification(`The candidate has processed your action! - ${selectedActionValue}`, employerId);
        }
    });
};

$('#deleteApplicationModal').on('hidden.bs.modal', function(e) {
    deleteApplicationBtn.removeAttribute('onclick');
});

const deleteRequest = (id) => {
    deleteApplicationBtn.setAttribute('onclick', `deleteApplication(${id})`);
    deleteApplicationModal.show();
};

const deleteApplication = (id) => {
    $.ajax({
        url:'/dashboard/ajax/delete-apply',
        type: 'POST',
        data: {apply_id: id},
        success: function(response) {
            document.getElementById(`application-${id}`).remove();
            deleteApplicationModal.hide();
        }
    });
};