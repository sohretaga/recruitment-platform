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
    searchEnabled: false,
});

document.querySelector('#action').addEventListener('showDropdown', () => {
    const applicantId = document.getElementById('employerAction').getAttribute('data-applicant-id');
    const hasValueAcceptRequestOtherDate =  document.getElementById(`has-value-request-other-date-${applicantId}`).value;

    if (hasValueAcceptRequestOtherDate) {
        showSuggestAndAcceptOption();
        hideInviteOption();

    } else {
        hideSuggestAndAcceptOption();
        showInviteOption();
    };
});

const hideSuggestAndAcceptOption = () => {
    setTimeout(() => {
        let acceptRequestOtherDate = document.querySelector(`.choices__list--dropdown div[data-value="ACCEPT_REQUEST_OTHER_DATE"]`);
        let suggestOtherDate = document.querySelector(`.choices__list--dropdown div[data-value="SUGGEST_OTHER_DATE"]`);
        acceptRequestOtherDate.classList.add('d-none');
        suggestOtherDate.classList.add('d-none');
    }, 1);
};

const showSuggestAndAcceptOption = () => {
    setTimeout(() => {
        let acceptRequestOtherDate = document.querySelector(`.choices__list--dropdown div[data-value="ACCEPT_REQUEST_OTHER_DATE"]`);
        let suggestOtherDate = document.querySelector(`.choices__list--dropdown div[data-value="SUGGEST_OTHER_DATE"]`);
        acceptRequestOtherDate.classList.remove('d-none');
        suggestOtherDate.classList.remove('d-none');
    }, 1);
};

const hideInviteOption = () => {
    setTimeout(() => {
        let invite = document.querySelector(`.choices__list--dropdown div[data-value="INVITE"]`);
        invite.classList.add('d-none');
    }, 1);
};

const showInviteOption = () => {
    setTimeout(() => {
        let invite = document.querySelector(`.choices__list--dropdown div[data-value="INVITE"]`);
        invite.classList.remove('d-none');
    }, 1);
};

flatpickr(inviteDateInput, {
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
    if (actions.value == 'INVITE' || actions.value == 'SUGGEST_OTHER_DATE') {
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
    applicantMessageModal.show();
};

const action = (id) => {
    const hasValueAction = document.getElementById(`has-value-action-${id}`).value;
    const hasValueAcceptRequestOtherDate =  document.getElementById(`has-value-request-other-date-${id}`).value;
    const hasValueInviteDate = document.getElementById(`has-value-invite-date-${id}`).value;

    if (hasValueAction == 'INVITE' || hasValueAction == 'SUGGEST_OTHER_DATE') {
        inviteDateInput.closest('div').style.display = 'inline';
        inviteDateInput.value = hasValueInviteDate;
    }else {
        inviteDateInput.closest('div').style.display = 'none';
        inviteDateInput.value = '';
    };

    if (hasValueAction && !hasValueAcceptRequestOtherDate) {
        actionChoices.setChoiceByValue(hasValueAction);
    }else {
        actionChoices.setChoiceByValue('SHORTLIST');
        inviteDateInput.closest('div').style.display = 'none';
        inviteDateInput.value = '';
    }

    document.getElementById('employerAction').setAttribute('data-applicant-id', id);
    const applicantName = document.getElementById(`applicant-name-${id}`).innerText;
    modalTitle.innerText = applicantName;
    sendActionBtn.setAttribute('onclick', `sendAction(${id})`);
    employerActionModal.show();
};

const sendAction = (id) => {
    const selectedActionValue = document.getElementById('action').value;
    const selectedInviteDateValue = document.getElementById('invite-date').value;

    if (selectedActionValue == 'INVITE' || selectedActionValue == 'SUGGEST_OTHER_DATE') {
        if (selectedInviteDateValue == '') {
            inviteDateInput.style.borderColor = '#DA3746';
            return;
        };
    };

    $.ajax({
        url: '/ajax/send-employer-action',
        type: 'POST',
        data: {
            applicant_id: id,
            action_value: selectedActionValue,
            invite_date: selectedInviteDateValue
        },
        success: function() {
            employerActionModal.hide();
            const asctionStatus = document.getElementById(`action-status-${id}`);
            const hasValueAcceptRequestOtherDate =  document.getElementById(`has-value-request-other-date-${id}`);
            const candidateId = document.getElementById(`candidate-user-${id}`).value;

            document.getElementById(`has-value-action-${id}`).value = selectedActionValue;
            document.getElementById(`has-value-invite-date-${id}`).value = selectedInviteDateValue;

            
            if (selectedActionValue == 'SHORTLIST') {
                asctionStatus.innerHTML = 'Shortlisted <i class="uil uil-user-check">';
                asctionStatus.classList = 'btn btn-primary';
                hasValueAcceptRequestOtherDate.value = '';

            } else if (selectedActionValue == 'DELIST') {
                asctionStatus.innerHTML = 'Delisted <i class="uil uil-times-circle">';
                asctionStatus.classList = 'btn btn-danger';
                hasValueAcceptRequestOtherDate.value = '';

            } else if (selectedActionValue == 'INVITE') {
                asctionStatus.innerHTML = `<span>Invited Date<br>${selectedInviteDateValue}</span> <i class="uil uil-clock-eight"></i>`;
                asctionStatus.classList = 'btn btn-success';
                hasValueAcceptRequestOtherDate.value = '';

            } else if (selectedActionValue == 'SUGGEST_OTHER_DATE') {
                asctionStatus.innerHTML = `<span>Another Date Suggested<br>${selectedInviteDateValue}</span> <i class="uil uil-clock-eight"></i>`;
                asctionStatus.classList = 'btn btn-success';
                hasValueAcceptRequestOtherDate.value = '';

            } else if (selectedActionValue == 'ACCEPT_REQUEST_OTHER_DATE') {
                asctionStatus.innerHTML = `<span>Requested Date Accepted<br>${hasValueAcceptRequestOtherDate.value}</span> <i class="uil uil-clock-eight"></i>`;
                asctionStatus.classList = 'btn btn-success';
            }
            
            sendNotification(candidateId, {
                message: `The employer has processed your application! - ${selectedActionValue}`,
                apply_id: id
            });
        }
    });
};