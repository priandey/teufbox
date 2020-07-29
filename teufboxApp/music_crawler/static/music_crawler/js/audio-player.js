/* Initializing audio elements in DOM */
let audioStream = document.createElement('audio');

/* Bindings audio events to vue player methods */
audioStream.addEventListener('ended', function(){
    musicPlayer.nextSong();
});

audioStream.ontimeupdate = function() {
    musicPlayer.updateTime();
};

audioStream.onloadedmetadata = function () {
    musicPlayer.setDuration();
};

/* Declaring vue element for player */
let musicPlayer = new Vue({
    el: '#musicPlayer',
    delimiters: ['<<<', '>>>'],
    data: {
        controls: {
            playing: false,
            audioEl: audioStream,
            currentTimePosition: "0",
            songDuration: "0"
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
        },

        nextSong: function() {
            if (this.playlist.currentSong.index < musicCache.musicList.length - 1) {
                let myAudio = this.controls.audioEl;
                this.playlist.currentSong.index += 1;
                this.loadSong();
                this.controls.playing = false;
            }
        },

        previousSong: function() {
            if (this.playlist.currentSong.index > 0) {
                let myAudio = this.controls.audioEl;
                this.playlist.currentSong.index -= 1;
                this.loadSong();
                this.controls.playing = false;
            }
        },

        updateTime: function() {
            this.controls.currentTimePosition = new String(this.controls.audioEl.currentTime);
            console.log(this.controls.currentTimePosition);
            console.log(this.controls.songDuration)
        },

        setDuration: function() {
            this.controls.songDuration = new String(this.controls.audioEl.duration);
        }
    }

});