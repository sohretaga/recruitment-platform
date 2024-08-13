const redirectUrl = () => {
    const checkboxes = document.querySelectorAll('#blog-categories input[type="checkbox"]');
    const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
    const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);

    window.location.assign(`/blog/?categories=${selectedValues.join(',')}#blog-list`)
};

const addCheckboxListener = (selector, callback) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', callback);
    });
};

addCheckboxListener('#blog-categories input[type="checkbox"]', redirectUrl); // Categories Listener

const likeBlog = (id) => {
    let likeIcon = document.getElementById('like-icon');
    let likeCount = document.getElementById('like-count');

    $.ajax({
        url: '/blog/ajax/like-blog',
        type: 'POST',
        data: {blog_id: id},
        success: (response) => {
            if (response.action == 'like'){
                likeIcon.classList.add('liked');
                likeCount.innerText = response.count;
            }
            else if(response.action == 'dislike') {
                likeIcon.classList.remove('liked');
                likeCount.innerText = response.count;
            };
        }
    })
}

const userInfoElement = document.getElementById('user-info');
const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated');
const signInModal = new bootstrap.Modal(document.getElementById('signinModal'));

const commentBox = document.getElementById('comments-box');
const blogCommentCount = document.getElementById('blog-comment-count');
const commentInput = document.getElementById('comment-input');

const sendComment = (id) => {
    if (isAuthenticated == 'yes') {
        $.ajax({
            url: '/blog/ajax/send-comment',
            type: 'POST',
            data: {
                blog_id: id,
                comment: commentInput.value
            },
            success: (response) => {
                commentInput.value = '';
                blogCommentCount.innerText = response.comment_count;
    
                commentBox.insertAdjacentHTML('afterbegin', `
                <div id="comment-${response.id}" class="mt-5">
                    <div class="d-sm-flex align-items-top">
                        <div class="flex-shrink-0">
                            <img class="rounded-circle avatar-md img-thumbnail" src="${response.user_profile_photo ? response.user_profile_photo:'/static/main/images/user/default-profile.jpg'}" alt="${response.user_full_name}" />
                        </div>
                        <div class="flex-grow-1 ms-sm-3">
                            <small class="float-end fs-12 text-muted"><i class="uil uil-clock"></i> ${response.timestamp}</small>
                            <a href="javascript:(0)" class="primary-link"><h6 class="fs-16 mt-sm-0 mt-3 mb-2"></h6></a>
                            <div class="d-flex">
                                <a href="/candidate/${response.username}" class="primary-link">
                                    <h6 class="fs-16 mt-sm-0 mt-3 mb-2">${response.user_full_name}</h6>
                                </a>
                                <div class="ms-3">
                                    <a href="javascript:void(0)" data-bs-toggle="tooltip" data-bs-placement="top" title="Edit">
                                        <i class="uil uil-edit" onclick="editComment('${response.id}')"></i>
                                    </a>
                                    <a href="javascript:void(0)" class="ms-2" style="color: #da3746 !important;" onclick="deleteRequest('${response.id}')" data-bs-toggle="tooltip" data-bs-placement="top" title="Delete">
                                        <i class="uil uil-trash-alt"></i>
                                    </a>
                                </div>
                            </div>
                            <p class="text-muted fst-italic mb-0" id="comment-text-${response.id}">${response.comment}</p>
                        </div>
                    </div>
                </div>`);
            }
        });
    }else {
        signInModal.show();
    };
}

const sendCommentBtn = document.getElementById('send-comment-btn');
const editCommentBtn = document.getElementById('edit-comment-btn');

const editComment = (id) => {
    let commentText = document.getElementById(`comment-text-${id}`).innerText;
    commentInput.value = commentText;
    
    sendCommentBtn.style.display = 'none';
    editCommentBtn.style.display = 'inline';

    editCommentBtn.setAttribute('onclick', `editRequest('${id}')`);

}

const editRequest = (id) => {
    $.ajax({
        url: '/blog/ajax/edit-comment',
        type: 'POST',
        data: {
            comment_id: id,
            edited_comment: commentInput.value
        },
        success: (response) => {
            let commentText = document.getElementById(`comment-text-${id}`);
            commentText.innerText = response.edited_comment;
            commentInput.value = '';

            sendCommentBtn.style.display = 'inline';
            editCommentBtn.style.display = 'none';

            editCommentBtn.removeAttribute('onclick');

            blogCommentCount.innerText = response.comment_count;
        }
    })
}

const deleteCommentModal = new bootstrap.Modal(document.getElementById('deleteCommentModal'));
const deleteCommentBtn = document.getElementById('delete-comment-btn');

$('#deleteCommentModal').on('hidden.bs.modal', function(e) {
    deleteCommentBtn.removeAttribute('onclick');
});

const deleteRequest = (id) => {
    deleteCommentBtn.setAttribute('onclick', `deleteComment(${id})`);
    deleteCommentModal.show();
};

const deleteComment = (id) => {
    $.ajax({
        url:'/blog/ajax/delete-comment',
        type: 'POST',
        data: {comment_id: id},
        success: (response) => {
            document.getElementById(`comment-${id}`).remove();
            deleteCommentModal.hide();
            blogCommentCount.innerText = response.comment_count;
        }
    });
};