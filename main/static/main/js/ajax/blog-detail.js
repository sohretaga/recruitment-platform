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