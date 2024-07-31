const csrf_token = document.getElementById('csrf-token').value;
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrf_token);
        $('body').css('cursor', 'wait');
    },
    complete: function () {
        $('body').css('cursor', 'default');
    },
    error: function () {
        console.error('Failure when operation performed...');
    }
});

const notificationToggle = document.getElementById('notification-toggle');
const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const userId = document.getElementById('user-id').value;

if(notificationToggle) {
    const WsUrl = `${wsProtocol}${window.location.host}/ws/notifications/${userId}/`;
    const notificationSocket = new WebSocket(WsUrl);
    const notificationList = document.getElementById('notification-list');
    const notificationCoutn = document.getElementById('notification-count');
    
    notificationSocket.onmessage = function(e) {
        notificationCoutn.classList.remove('d-none');

        if(notificationCoutn.innerText){
            notificationCoutn.innerText = parseInt(notificationCoutn.innerText)+1;
        }else {
            notificationCoutn.innerText = 1;
        };
    };

    notificationToggle.addEventListener('show.bs.dropdown', function() {
        $.ajax({
            url: '/ajax/get-notifications',
            type: 'POST',
            success: function(response) {
                const notifications = JSON.parse(response.notifications);
                loadNotifications(notifications);
            }
        });
    });
};

const loadNotifications = (data) => {
    const notificationList = document.getElementById('notification-list');
    const notificationCount = document.getElementById('notification-count');

    notificationList.innerHTML = '';
    notificationCount.innerText = '';
    notificationCount.classList.add('d-none');

    data.forEach(notification => {
        const newNotificationHTML = `
            <a href="${notification.related_data ? `${notification.related_data}`:'javascript:void(0)'}" class="notification-item d-block ${notification.related_data ? 'text-dark':'deactive-notification'}">
                <div class="d-flex align-items-center">
                    <div class="flex-shrink-0 me-3">
                        <img src="${notification.profile_photo ? `${notification.profile_photo}`:'/static/main/images/featured-job/default-company-img.jpeg'}" class="rounded-circle avatar-xs" alt="user-pic">
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="mt-0 mb-1 fs-14">${notification.content}</h6>
                        <p class="text-muted mb-0 fs-12"><i class="mdi mdi-clock-outline"></i> <span>${notification.timestamp}</span></p>
                    </div>
                </div>
            </a>
        `;
        notificationList.innerHTML = notificationList.innerHTML + newNotificationHTML;
    });
};

const sendNotification = (target_id, args) => {
    const targetWsUrl = `${wsProtocol}${window.location.host}/ws/send-notifications/${target_id}/`;
    const targetSocket = new WebSocket(targetWsUrl);

    targetSocket.onopen = () => {
        targetSocket.send(
            JSON.stringify(args)
        );
    };
};

const subscribeBtn = document.getElementById('subscribebtn');
const subscribeAlert = document.getElementById('subscribe-alert');
subscribeBtn.addEventListener('click', () => {
    const subscribeInput = document.getElementById('subscribe');
    if (subscribeInput.value) {
        $.ajax({
            url:'/ajax/subscribe',
            type: 'POST',
            data: {email: subscribeInput.value},
            success: () => {
                subscribeInput.value = '';
                subscribeAlert.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    You have subscribed!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>`;
            }
        });
    };
});