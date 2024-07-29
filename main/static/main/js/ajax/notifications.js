const selectAllBtn = document.getElementById('select-all-btn');
const clearAllBtn = document.getElementById('clear-all-btn');
const deleteNotificationCheckbox = document.querySelectorAll('.notification-delete');
const deleteNotificationModal = new bootstrap.Modal(document.getElementById('deleteNotificationModal'));
const deleteNotificationBtn = document.getElementById('delete-notification-btn');

const choicesSingleFilterOrderby = new Choices('#choices-single-filter-orderby');
const choicesCandidatePage = new Choices('#choices-candidate-page');


selectAllBtn.addEventListener('click', () => {
    deleteNotificationCheckbox.forEach((checkbox) => {
        const input = checkbox.querySelector('input');

        if(input.checked) {
            input.checked = false;
        }else{
            input.checked = true;
        };
    });
})

clearAllBtn.addEventListener('click', () => {

    clearAllBtn.innerHTML = '<i class="uil uil-trash-alt"></i> Delete';
    clearAllBtn.setAttribute('onclick', 'bulkDelete()');

    deleteNotificationCheckbox.forEach((checkbox) => {
        checkbox.classList.replace('d-none', 'd-flex');
        selectAllBtn.classList.replace('d-none', 'd-flex');
    });
});

const bulkDelete = () => {
    const selectedNotifications = document.querySelectorAll(".notification-delete input:checked");
    const notificationIdList = new Array();

    selectedNotifications.forEach((checkbox) => {
        const parentDiv = checkbox.closest('div.notification');
        notificationIdList.push(parentDiv.getAttribute('data-id'));
    });

    if (notificationIdList) {
        $.ajax({
            url: '/ajax/delete-notifications',
            type: 'POST',
            data: {id_list:JSON.stringify(notificationIdList)},
            success: function(response) {
                window.location.reload();
            }
        });
    };
};

$('#deleteNotificationModal').on('hidden.bs.modal', function(e) {
    deleteNotificationBtn.removeAttribute('onclick');
});

const deleteRequest = (id) => {
    deleteNotificationBtn.setAttribute('onclick', `deleteNotification(${id})`);
    deleteNotificationModal.show();
};

const deleteNotification = (id) => {
    $.ajax({
        url:'/ajax/delete-notification',
        type: 'POST',
        data: {notification_id: id},
        success: function(response) {
            document.getElementById(`notification-${id}`).remove();
            deleteNotificationModal.hide();
        }
    });
};