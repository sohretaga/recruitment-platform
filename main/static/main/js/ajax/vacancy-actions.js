const userInfoElement = document.getElementById('user-info');
const modalDeleteYesBtn = document.getElementById('delete-yes');

const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated');
const signInModal = new bootstrap.Modal(document.getElementById('signinModal'));

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
                vacancy: id,
            }
        });

    }else {
        signInModal.show();
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
const deleteApply = new bootstrap.Modal(document.getElementById('deleteApply'));

const sendApplicationBtn = document.getElementById('send-application');
const deleteApplicationBtn = document.getElementById('delete-application');

const sendApplication = (id) => {
    const applyNowBtn = document.getElementById(`apply-now-${id}`);
    const message = document.getElementById('apply-message');
    const cv = document.getElementById('apply-cv');
    const messageWarning = document.getElementById('message-warning');
    const formData = new FormData();
    formData.append('vacancy', id);
    formData.append('message', message.value);
    if (cv.files.length > 0) {
        formData.append('cv', cv.files[0]);
    };

    if (message.value) {
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

                applyNowBtn.id = `delete-apply-${id}`;
                applyNowBtn.innerHTML = 'Delete Apply  <i class="mdi mdi-chevron-double-right">';

                messageWarning.style.display = 'none';
                message.style.borderColor = '';
            }
        });
    } else {
        message.style.borderColor = '#DA3746';
        messageWarning.style.display = 'inline';
    };
};

const deleteApplication = (id) => {
    const deleteApplyBtn = document.getElementById(`delete-apply-${id}`);

    $.ajax({
        url: '/ajax/apply',
        type: 'POST',
        data: {vacancy: id},
        success: function() {
            deleteApply.hide();
            deleteApplyBtn.id = `apply-now-${id}`;
            deleteApplyBtn.innerHTML = 'Apply Now  <i class="mdi mdi-chevron-double-right">';
        }
    });
};

const apply = (id) => {

    if (isAuthenticated == 'yes'){
        const apply = document.getElementById(`apply-now-${id}`);

        if (apply) {
            sendApplicationBtn.setAttribute("onclick", `sendApplication(${id})`);
            applyNow.show();
        } else {
            deleteApplicationBtn.setAttribute("onclick", `deleteApplication(${id})`);
            deleteApply.show();
        };
    } else {
        signInModal.show();
    };
};

$('#applyNow').on('hidden.bs.modal', function(e) {
    document.getElementById('apply-message').style.borderColor = '';
    document.getElementById('message-warning').style.display ='none';
    sendApplicationBtn.removeAttribute('onclick');
});

$('#deleteApply').on('hidden.bs.modal', function(e) {
    deleteApplicationBtn.removeAttribute('onclick');
});

document.getElementById('apply-message').addEventListener('input', function() {
    document.getElementById('apply-message').style.borderColor = '';
    document.getElementById('message-warning').style.display ='none';
});