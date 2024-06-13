document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); 
    
    var subject = document.getElementById('subject').value;
    var content = document.getElementById('field0').value;
    
    var link = "mailto:sunkencouch67@gmail.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(content)

    window.location.href = link;
    
});