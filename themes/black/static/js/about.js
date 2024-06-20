document.getElementById('contact-form').addEventListener('submit', async (evt) => {

    evt.preventDefault()

    const aboutField = document.getElementById('contact-about').value
    const fromField = document.getElementById('contact-from').value
    const bodyField = document.getElementById('contact-body').value

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/forward_email")
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(JSON.stringify({
        about: aboutField,
        body: bodyField,
        from: fromField
    }))

    document.getElementById('contact-form').style.display = 'none'
    document.getElementById('info-text').style.display = 'block'

})