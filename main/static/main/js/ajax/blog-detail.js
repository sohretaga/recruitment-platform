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

const commentBox = document.getElementById('comments-box');
const blogCommentCount = document.getElementById('blog-comment-count');

const sendComment = (id) => {
    let commentInput = document.getElementById('comment-input');

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

            commentBox.insertAdjacentHTML('beforebegin', `
            <div class="mt-5">
                <div class="d-sm-flex align-items-top">
                    <div class="flex-shrink-0">
                        <img class="rounded-circle avatar-md img-thumbnail" src="${response.user_profile_photo ? response.user_profile_photo:'/static/main/images/user/default-profile.jpg'}" alt="${response.user_full_name}" />
                    </div>
                    <div class="flex-grow-1 ms-sm-3">
                        <small class="float-end fs-12 text-muted"><i class="uil uil-clock"></i> ${response.timestamp}</small>
                        <a href="javascript:(0)" class="primary-link"><h6 class="fs-16 mt-sm-0 mt-3 mb-2">${response.user_full_name}</h6></a>
                        <p class="text-muted fst-italic mb-0">${response.comment}</p>
                    </div>
                </div>
            </div>`);
        }
    })
}