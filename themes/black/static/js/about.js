document.getElementById('contact-form').addEventListener('submit', async (evt) => {

    evt.preventDefault()
    document.getElementById('contact-form').style.display = 'none'

    const aboutField = document.getElementById('contact-about').value
    const fromField = document.getElementById('contact-from').value
    const bodyField = document.getElementById('contact-body').value
    const recaptchaToken = grecaptcha.getResponse();

    if (!recaptchaToken) {
        alert("Please complete the reCAPTCHA.");
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/forward_email")
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(JSON.stringify({
        about: aboutField,
        body: bodyField,
        from: fromField,
        recaptchaToken: recaptchaToken
    }))

    var infoText = document.getElementById('info-text')

    infoText.style.display = 'block'

    xhr.onload = function() {
        if (xhr.status != 200) {
            infoText.innerHTML = "An unexpected error occurred. Please report this error to the developer."
            return;
        }
    };

})