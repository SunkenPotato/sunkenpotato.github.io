function submitForm() {
    var subj = $("contact-about").val()
    var content = $("contact-text").val()

    var link = "mailto:sunkencouch67@gmail.com?subject=" + subj + "&body=" + content

    window.open(link, '_self')
}