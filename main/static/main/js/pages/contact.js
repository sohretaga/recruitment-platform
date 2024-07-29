
const validateForm = () => {
    var name = document.forms["contactForm"]["name"].value;
    var email = document.forms["contactForm"]["email"].value;
    var subject = document.forms["contactForm"]["subject"].value;
    var message = document.forms["contactForm"]["message"].value;

    document.getElementById("error-msg").style.opacity = 0;
    document.getElementById("error-msg").innerHTML = "";

    if (name == "" || name == null) {
        document.getElementById("error-msg").innerHTML =
            "<div class='alert alert-danger error_message'>" +
            "<i class='mdi mdi-alert'></i> Please enter a name</div>";
        fadeIn();
        return false;
    }

    if (email == "" || email == null) {
        document.getElementById("error-msg").innerHTML =
            "<div class='alert alert-danger error_message'>" +
            "<i class='mdi mdi-alert'></i> Please enter an email</div>";
        fadeIn();
        return false;
    }

    if (subject == "" || subject == null) {
        document.getElementById("error-msg").innerHTML =
            "<div class='alert alert-danger error_message'>" +
            "<i class='mdi mdi-alert'></i> Please enter a subject</div>";
        fadeIn();
        return false;
    }

    if (message == "" || message == null) {
        document.getElementById("error-msg").innerHTML =
            "<div class='alert alert-danger error_message'>" +
            "<i class='mdi mdi-alert'></i> Please enter a message</div>";
        fadeIn();
        return false;
    }
}

function fadeIn() {
    var errorMsg = document.getElementById("error-msg");
    var opacity = 0;
    var interval = setInterval(function() {
        if (opacity < 1) {
            opacity += 0.5;
            errorMsg.style.opacity = opacity;
        } else {
            clearInterval(interval);
        }
    }, 200);
}
