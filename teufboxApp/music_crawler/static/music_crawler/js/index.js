function remove_button(button_id) {
    var element = document.getElementById(button_id);
    element.parentNode.removeChild(element);
}

$('input.downloadButton').click(function(event){
    event.preventDefault();
    let form = this.parentElement;
    let formData =
        {
            'csrfmiddlewaretoken': form[0].defaultValue,
            'title': form[1].defaultValue,
            'artist': form[2].defaultValue,
            'thumbnail': form[3].defaultValue,
            'id': form[4].defaultValue
        };
    var buttonId = this.id
    var progressBar = this.parentElement.nextSibling;
    progressBar.hidden = false;
    $.post('/register_song', formData, function(data) {
        console.log("SERVER : " + data.status);
        progressBar.hidden = true;
        $("<p class='notification'>" + data.status + "</p>").insertAfter(progressBar);
        if (data.error != true) {
            remove_button(buttonId);
        }
    });

});