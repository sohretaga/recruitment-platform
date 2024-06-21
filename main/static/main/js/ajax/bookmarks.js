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