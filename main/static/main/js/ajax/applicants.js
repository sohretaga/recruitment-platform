$('#applicantMessage').on('hidden.bs.modal', function(e) {
    document.getElementById('applicant-message').innerText = '';
    document.getElementById('applicant-modal-title').innerText = '';
});

const applicantMessage = new bootstrap.Modal(document.getElementById('applicantMessage'));

const message = (message, applicant) => {
    document.getElementById('applicant-message').innerText = message;
    document.getElementById('applicant-modal-title').innerText = applicant;
    applicantMessage.show()
}