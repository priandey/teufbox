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
    musicCache.musicList.push({
        'title': formData['title'],
        'yt_id': formData['id'],
        'is_local': false,
        'formData':formData
    });
    $.post('/music_cache', formData, function(data) {
        progressBar.hidden = true;
        $("<p class='notification'>" + data.status + "</p>").insertAfter(progressBar);
        if (data.error != true) {
            remove_button(buttonId);
        }
    });

});

let searchYoutube = new Vue({
    el: '#SearchYoutube',
    delimiters: ['<<<', '>>>'],
    data: {
        resultList : new Array(),
        keywords: new String(),
        searching: false,
    },
    methods: {
        getResult: function() {
            musicCache.refreshList();
            let output = searchYoutube.resultList;
            searchYoutube.searching = true;
            output.splice(0, output.length);
            axios
                .get('/search_song?keywords='+searchYoutube.keywords)
                .then(function(response) {
                    searchYoutube.searching = false;
                    response.data.forEach(function (item) {
                        output.push(item);
                    })
                })
        },
        addToCache: function(music) { /* TODO : Forbid adding more than once yt_id in the list properly (handle server error)*/
            console.log(music);
            $.post('/music_cache', {
                title: music.name,
                id: music.id,
                thumbnail: music.thumbnail
            }, function(data) {
                musicCache.refreshList();
                print(data.getAllResponseHeaders())
            })
        }
    }
});

/* TODO : Amélioration du téléchargement pour éviter la simultanéité : await ? */
let musicCache = new Vue(
{
    el: '#musicCache',
    delimiters: ['<<<', '>>>'],
    data: {
        musicList: new Array(),
    },
    mounted () {
        this.refreshList()
    },
    methods: {

        deleteItem: function(index) {
            axios
                .delete('/music_cache?id='+musicCache.musicList[index].yt_id);
            musicCache.musicList.splice(index,1);
        },

        emptyCache: function() {
            /* Empty the music cache both on front and back end */
            musicCache.musicList.forEach(function(item, index) {
                musicCache.deleteItem(index)
            })
        },

        refreshList: function() {
            /* Refresh music cache with backend data */
            this.musicList.splice(0, this.musicList.length);
            axios
                .get('/music_cache?music=all')
                .then(response => (
                        response.data.forEach(function (item){
                            musicCache.musicList.push(item);
                        })
                    )
                )
        },

        download: function (music) {
            if (music.is_local === false) {
                music.is_downloading = true;
                let params = {
                    id: music.yt_id,
                    thumbnail: music.thumbnail
                };
                $.post("/register_song", params, function (data) {
                    musicCache.refreshList()
                })
            }
        },

        downloadAll: function() {
            /* Download all the elements on the list, and flag them as downloaded and local */
            musicCache.musicList.forEach(function(music) {
                musicCache.download(music);
            });
        },
    }
});