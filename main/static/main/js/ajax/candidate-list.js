const choicesSingleLocation = new Choices('#choices-single-location');
const choicesSingleCategories = new Choices('#choices-single-categories');
const choicesSingleFilterOrderby = new Choices('#choices-single-filter-orderby');
const choicesCandidatePage = new Choices('#choices-candidate-page');

const userInfoElement = document.getElementById('user-info');
const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated');
const signInModal = new bootstrap.Modal(document.getElementById('signinModal'));

const addCandidateBookmark = (id) => {

    if (isAuthenticated == 'yes'){
        const candidateBox = document.getElementById(`candidate-${id}`);

        if (candidateBox.classList.contains('bookmark-post')) {
            candidateBox.classList.remove('bookmark-post');
        }else {
            candidateBox.classList.add('bookmark-post');
        }
    
        $.ajax({
            url: '/ajax/add-candidate-bookmark',
            type: 'POST',
            data: {
                candidate: id,
            }
        });

    }else {
        signInModal.show();
    }
};