let audioStream = document.createElement('audio');
audioStream.setAttribute('v-on:ended', 'nextSong');

let musicPlayer = new Vue({
    el: '#musicPlayer',
    delimiters: ['<<<', '>>>'],
    data: {
        controls: {
            playing: false,
            audioEl: audioStream,
        },
        playlist: {
            currentSong: {
                index: 0,
                song: '',

            }
        }
    }, /* TODO : Find a way to link music-cache and playlist */
    mounted () {
        setTimeout(this.refreshSong, 500);
        setTimeout(this.loadSong, 500)
    },

    updated () {
        this.refreshSong()
    },

    methods: {
        refreshSong: function() {
            let index = this.playlist.currentSong.index;
            this.playlist.currentSong.song = musicCache.musicList[index]
        },

        loadSong: function() {
            this.refreshSong();
            let myAudio = this.controls.audioEl;
            if(myAudio.canPlayType('audio/mpeg')) {
                myAudio.setAttribute('src', this.playlist.currentSong.song.url);
            }
        },

        playSong: function() {
            this.refreshSong();
            let myAudio = this.controls.audioEl;
            myAudio.play();
            this.controls.playing = true;
        },

        pauseSong: function () {
            let myAudio = this.controls.audioEl;
            myAudio.pause();
            this.controls.playing = false;
        }
    }

});