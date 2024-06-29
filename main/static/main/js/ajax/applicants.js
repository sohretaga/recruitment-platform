const applicantMessageModal = new bootstrap.Modal(document.getElementById('applicantMessage'));
const employerActionModal = new bootstrap.Modal(document.getElementById('employerAction'));

const applicantMessage = document.getElementById('applicant-message');
const applicantModalTitle = document.getElementById('applicant-modal-title');

const actions = document.getElementById("action");
const inviteDateInput = document.getElementById('invite-date');
const theme = localStorage.getItem('theme');
const darkThemeLink = document.getElementById('flatpickr-dark');
const modalTitle = document.getElementById('modal-title');
const sendActionBtn = document.getElementById('send-action-btn');

const locationChoices = new Choices('#choices-single-location');
const singleFilterChoices = new Choices('#choices-single-filter-orderby');
const actionChoices = new Choices('#action', {
    shouldSort: false,
    shouldSortItems: false,
    searchEnabled: false
});

flatpickr(inviteDateInput, {
    enableTime: true,
    dateFormat: "d-m-Y H:i",
    time_24hr: true
});


if (theme == 'dark') {
    darkThemeLink.disabled = false;
} else {
    darkThemeLink.disabled = true;
};

actions.addEventListener('change', function() {
    if (actions.value == 'INVITE') {
        inviteDateInput.closest('div').style.display = 'inline';
    } else {
        inviteDateInput.closest('div').style.display = 'none';
    };
});

inviteDateInput.addEventListener('change', function () {
    inviteDateInput.style.borderColor = '';
});

$('#applicantMessage').on('hidden.bs.modal', function (e) {
    applicantMessage.innerText = '';
    applicantModalTitle.innerText = '';
});

$('#employerAction').on('hidden.bs.modal', function (e) {
    modalTitle.innerText = '';
    inviteDateInput.value = '';
    inviteDateInput.style.borderColor = '';
    inviteDateInput.closest('div').style.display = 'none';
    actionChoices.setChoiceByValue('SHORTLIST');
    sendActionBtn.removeAttribute('onclick');
});

const message = (id) => {
    const message = document.getElementById(`message-${id}`).value;
    const full_name = document.getElementById(`full-name-${id}`).value;

    applicantMessage.innerText = message;
    applicantModalTitle.innerText = full_name;
    applicantMessageModal.show()
};

const action = (id) => {
    const hasValueAction = document.getElementById(`has-value-action-${id}`).value;
    const hasValueInviteDate = document.getElementById(`has-value-invite-date-${id}`).value;

    if (hasValueAction) {
        actionChoices.setChoiceByValue(hasValueAction);
    };

    if (hasValueAction == 'INVITE') {
        inviteDateInput.closest('div').style.display = 'inline';
        inviteDateInput.value = hasValueInviteDate;
    };

    const applicantName = document.getElementById(`applicant-name-${id}`).innerText;
    modalTitle.innerText = applicantName;
    sendActionBtn.setAttribute('onclick', `sendAction(${id})`);
    employerActionModal.show();
};

const sendAction = (id) => {
    const selectedActionValue = document.getElementById('action').value;
    const selectedInviteDateVale = document.getElementById('invite-date').value;

    if (selectedActionValue == 'INVITE' && selectedInviteDateVale == '') {
        inviteDateInput.style.borderColor = '#DA3746';
        return;
    };

    $.ajax({
        url: '/ajax/send-employer-action',
        type: 'POST',
        data: {
            applicant_id: id,
            action_value: selectedActionValue,
            invite_date: selectedInviteDateVale
        },
        success: function() {
            employerActionModal.hide();
            const asctionStatus = document.getElementById(`action-status-${id}`);
            document.getElementById(`has-value-action-${id}`).value = selectedActionValue;
            document.getElementById(`has-value-invite-date-${id}`).value = selectedInviteDateVale;
            
            if (selectedActionValue == 'SHORTLIST') {
                asctionStatus.innerHTML = 'Shortlisted <i class="uil uil-user-check">';

            } else if (selectedActionValue == 'DELIST') {
                asctionStatus.innerHTML = 'Delisted <i class="uil uil-user-check">';

            } else if (selectedActionValue == 'INVITE') {
                asctionStatus.innerHTML = 'Invited <i class="uil uil-user-check">';
            };
        }
    });
};