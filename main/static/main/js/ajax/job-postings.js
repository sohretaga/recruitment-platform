const choicesSingleFilterOrderby = new Choices('#choices-single-filter-orderby');
const choicesCandidatePage = new Choices('#choices-candidate-page');
const deleteVacancyBtn = document.getElementById('delete-vacancy-btn');
const deleteVacancyModal = new bootstrap.Modal(document.getElementById('deleteVacancyModal'));


$('#deleteVacancyModal').on('hidden.bs.modal', function(e) {
    deleteVacancyBtn.removeAttribute('onclick');
});

const deleteRequest = (id) => {
    deleteVacancyBtn.setAttribute('onclick', `deleteVacancy(${id})`);
    deleteVacancyModal.show();
};

const deleteVacancy = (id) => {
    $.ajax({
        url:'/dashboard/ajax/delete-vacancy',
        type: 'POST',
        data: {vacancy_id: id},
        success: function(response) {
            document.getElementById(`vacancy-${id}`).remove();
            deleteVacancyModal.hide();
        }
    });
};