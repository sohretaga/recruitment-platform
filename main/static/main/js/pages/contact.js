// function validateForm(){var e=document.forms.myForm.name.value,t=document.forms.myForm.email.value,r=document.forms.myForm.comments.value;if(document.getElementById("error-msg").style.opacity=0,(document.getElementById("error-msg").innerHTML="")==e||null==e)return document.getElementById("error-msg").innerHTML="<div class='alert alert-danger error_message'><i  data-feather='home' class='icon-sm align-middle me-2'></i> Please enter a name</div>",fadeIn(),!1;if(""==t||null==t)return document.getElementById("error-msg").innerHTML="<div class='alert alert-danger error_message'><i  data-feather='alert-triangle' class='icon-sm align-middle me-2'></i> Please enter a email</div>",fadeIn(),!1;if(""==r||null==r)return document.getElementById("error-msg").innerHTML="<div class='alert alert-danger error_message'><i class='mdi mdi-alert'></i> Please enter a Message</div>",fadeIn(),!1;var n=new XMLHttpRequest;return n.onreadystatechange=function(){4==this.readyState&&200==this.status&&(document.getElementById("simple-msg").innerHTML=this.responseText,document.forms.myForm.name.value="",document.forms.myForm.email.value="",document.forms.myForm.comments.value="")}, /* n.open("POST","assets/php/contact.php",!0),n.setRequestHeader("Content-type","application/x-www-form-urlencoded"),n.send("name="+e+"&email="+t+"&comments="+r), */ !1}function fadeIn(){var e=document.getElementById("error-msg"),t=0,r=setInterval(function(){t<1?(t+=.5,e.style.opacity=t):clearInterval(r)},200)}

function validateForm() {
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
