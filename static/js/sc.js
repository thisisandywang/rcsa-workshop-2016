$("#cs").click( function() {
    $(this).hide();
    $("#input-email").show();
});

$("#email-input").keyup(function(event) {
    if (event.keyCode == 13) {
        $("#submit-button").click();
    }
});

$("#submit-button").click( function() {
    email = document.getElementById('email-input').value;
    verify(email);
});

function verify(email) {
    var n = email.length;
    console.log(email.substring(n-12))
    if (email.substring(n-12).toLowerCase() == "berkeley.edu") {
        window.location.href = "/scholarconnect/cs-results/";
    } else {
        $("#error-message").show();
    }
}