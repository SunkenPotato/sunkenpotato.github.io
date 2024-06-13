function submitForm() {

    console.log("sending request")

    var subject = document.getElementById("contact-about").value
    var body = document.getElementById("contact-text").value
    var reply = document.getElementById("reply").value

    var xhr = new XMLHttpRequest()
    xhr.open("POST", "http://127.0.0.1:5000/forward_email", true)
    xhr.send(`{"subject": "${subject}", "body": "${body}", "reply": "${reply}"}`)

    updateForm()

}

function updateForm() {
    form.style.display = "none"
    document.getElementById("success").style.display = "block"
}

const form = document.getElementById("ctf")
form.addEventListener("submit", event => {
    event.preventDefault()

    submitForm()
})