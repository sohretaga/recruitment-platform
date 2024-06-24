const userInfoElement = document.getElementById('user-info');
const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated');
const signInModal = new bootstrap.Modal(document.getElementById('signinModal'));
const modalDeleteYesBtn = document.getElementById('delete-yes');

const addBookmark = (id) => {

    if (isAuthenticated == 'yes'){
        const vacancyBox = document.getElementById(`vacancy-${id}`);

        if (vacancyBox.classList.contains('bookmark-post')) {
            vacancyBox.classList.remove('bookmark-post');
        }else {
            vacancyBox.classList.add('bookmark-post');
        }
    
        $.ajax({
            url: '/ajax/add-bookmark',
            type: 'POST',
            data: {
                'vacancy': id,
            }
        });

    }else {
        signInModal.show()
    }
};

const addBookmarkWithPopup = (id) => {
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    const vacancyBox = document.getElementById(`vacancy-${id}`);

    if (vacancyBox.classList.contains('bookmark-post')){
        deleteModal.show()
        modalDeleteYesBtn.setAttribute("onclick", `addBookmark(${id})`);
    }else {
        addBookmark(id);
    };
};


const applyNow = new bootstrap.Modal(document.getElementById('applyNow'));
const sendApplicationBtn = document.getElementById('send-application');

const sendApplication = (id) => {
    const applyNowBtn = document.getElementById('applyNow');
    const message = document.getElementById('apply-message');
    const cv = document.getElementById('apply-cv');
    const formData = new FormData();
    formData.append('vacancy', id);
    formData.append('message', message.value);
    if (cv.files.length > 0) {
        formData.append('cv', cv.files[0]);
    };
    
    $.ajax({
        url: '/ajax/apply',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function() {
            applyNow.hide();
            message.value = '';
            cv.value = '';
            applyNowBtn.id = 'deleteApply';
            applyNowBtn.innerText = 'Delete Apply';
        }
    });

};

const apply = (id) => {
    const vacancyBox = document.getElementById(`vacancy-${id}`);

    sendApplicationBtn.setAttribute("onclick", `sendApplication(${id})`);
};