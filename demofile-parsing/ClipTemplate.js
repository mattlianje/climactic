const fs = require("fs");

class ClipTemplate {
  constructor(videoId, type) {
    this.demoGameStart = null;
    this.streamGameStart = null;
    this.videoId = videoId;
    this.embeddedClips = "";
    this.type = type || "youtube"; // by default assume it is a youtube clip
  }

  addRoundHighlights(timeRanges, demoGameStart, streamGameStart, roundIndex) {
    var roundTitle = ` \n <h2> Round ${roundIndex} </h2> \n`;
    if (this.type === "youtube") {
      var youtubeLinks = this.getYoutubeLinks(timeRanges, demoGameStart, streamGameStart);
      this.embeddedClips = this.embeddedClips + roundTitle;
      for (var i = 0; i < youtubeLinks.length; i++) {
        this.embeddedClips = this.embeddedClips + this.youtubeIframe(youtubeLinks[i]);
      }
    }
  }

  youtubeIframe(src) {
    return(
      `
      <iframe
        width="560"
        height="315" 
        src="${src}"
        frameborder="0"
        allow="accelerometer;
        autoplay;
        encrypted-media;
        gyroscope;
        picture-in-picture"
        allowfullscreen>
      </iframe>
      `
    )
  }

  getYoutubeLinks(timeRanges, demoGameStart, streamGameStart) {
    var result = [];
    for (var i = 0; i < timeRanges.length; i++) {
      var start = Math.floor(timeRanges[i][0] - demoGameStart + streamGameStart);
      var end = Math.floor(timeRanges[i][1] - demoGameStart + streamGameStart);
      var youtubeLink = `https://www.youtube.com/embed/${this.videoId}?start=${start}&end=${end}`;
      result.push(youtubeLink);
    }
    return result;
  }

  getHTML() {
    return(
      `
      <html>
        ${this.embeddedClips}
      </html>
      `
    )
  }

  writeToFile(filename) {
    fs.writeFile(filename, this.getHTML(), (err) => {
      if (err) console.log(err);
      console.log("successfully written");
    });
  }


}

module.exports = ClipTemplate;