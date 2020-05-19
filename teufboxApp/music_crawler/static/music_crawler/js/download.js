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
    myApp.musicList.push({
       'title': formData['title'],
        'yt_id': formData['id'],
        'is_local': false,
    });
    $.post('/music_cache', formData, function(data) {
        progressBar.hidden = true;
        $("<p class='notification'>" + data.status + "</p>").insertAfter(progressBar);
        if (data.error != true) {
            remove_button(buttonId);
        }
    });

});

/* TODO : Télécharger récursivement les items de musiclist s'ils ne sont pas déjà présents en local. */
let myApp = new Vue(
{
    el: '#musicCache',
    delimiters: ['<<<', '>>>'],
    data: {
        musicList: new Array(),
    },
    mounted () {
        /* Get all music cache  */
        axios
            .get('/music_cache?music=all')
            .then(response => (
                response.data.forEach(function (item){
                    myApp.musicList.push(item);
                })
                )
            )
    },
    methods: {
        deleteItem: function(index) {
            axios
                .delete('/music_cache?id='+myApp.musicList[index].yt_id);
            myApp.musicList.splice(index,1);
        }
    }
});