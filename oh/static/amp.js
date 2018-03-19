
Handlebars.registerHelper("grey", function(value) {
    var level = 255-parseInt(parseFloat(value) * 255);

    return "rgb(" + level + "," + level + "," + level + ")"
});


function timeUpdateListener() {
    var player = document.getElementById('audioplayer');
    var end = player.getAttribute("data-end");

    if(this.currentTime >= end) {
        this.pause();
    }
}

function playSegment(start, end) {
    var player = document.getElementById('audioplayer');

    player.setAttribute("data-start", start);
    player.setAttribute("data-end", end);

    player.currentTime = start;
    player.play();
}

// create an audio player for a topic
Handlebars.registerHelper("topicplayer", function(transcript,  audiourl, start, end) {
    var start = parseInt(start);
    var end = parseInt(end);
    var b = transcript[start].start_time/1000;
    var e = transcript[end-1].end_time/1000;

    result = "<div class=audiocontrols>";
    result += "<button class='btn btn-secondary mr-1' onclick=\"playSegment(" + b + ", " + e + ")\">Play</button>";
    result += "<button class='btn btn-secondary mr-1' onclick=\"document.getElementById('audioplayer').pause()\">Pause</button>";
    result += "</div>";

    return new Handlebars.SafeString(result);

});

Handlebars.registerHelper("topic", function(speakers, transcript, audiourl, start, end) {
    var start = parseInt(start);
    var end = parseInt(end);

    var result = "<ul class='topic'>";
    for(var i=start; i<end; i++) {
        var b = transcript[i].start_time;
        var e = transcript[i].end_time;

        var spkr = "Multiple";
        for(var j=0; j<speakers.length; j++) {
            if (speakers[j].id === transcript[i].speaker_id) {
                spkr = speakers[j].name;
            }
        }

        result += "<li><strong>" + spkr + ":</strong> " + transcript[i].text + "</li>";
    }
    result += "</ul>";

    return new Handlebars.SafeString(result);
});
