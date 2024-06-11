const addBookmark = (id) => {
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
};