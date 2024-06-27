$('#applicantMessage').on('hidden.bs.modal', function(e) {
    document.getElementById('applicant-message').innerText = '';
    document.getElementById('applicant-modal-title').innerText = '';
});

const applicantMessage = new bootstrap.Modal(document.getElementById('applicantMessage'));

const message = (id) => {
    const message = document.getElementById(`message-${id}`).value;
    const full_name = document.getElementById(`full-name-${id}`).value;

    document.getElementById('applicant-message').innerText = message;
    document.getElementById('applicant-modal-title').innerText = full_name;
    applicantMessage.show()
}