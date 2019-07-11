const demofile = require("demofile");
const asciichart = require('asciichart');

class Round {

  constructor (startTime, endTime, keyEvents) {
    this.startTime = startTime || null;
    this.endTime = endTime || null;
    this.keyEvents = keyEvents || [];
    this.eventRates = [];
    this.highRateTimes = [];
    this.highlights = [];
  }

  // check if a time is within the round
  inRound(time) {
    return this.startTime <= time && this.endTime >= time;
  }

  pushKeyEvent(keyEvent) {
    this.keyEvents.push(keyEvent);
  }

  sortKeyEvents() {
    this.keyEvents.sort(this.compare);
  }

  compare( a, b ) {
    if ( a.time < b.time ){
      return -1;
    }
    if ( a.time > b.time ){
      return 1;
    }
    return 0;
  }

  calculateEventRates() {
    var i;
    for (i = 0; i+1 < this.keyEvents.length; i++) {
      var deltaTime = this.keyEvents[i+1].time - this.keyEvents[i].time;
      var rate = deltaTime > 0 ? 1/deltaTime : 0;
      this.eventRates.push(rate);
    }
  }

  getHighRateTimes() {
    // find average rate
    var total = 0;

    for(var i = 0; i < this.eventRates.length; i++) {
        total += this.eventRates[i];
    }
    var avg = total / this.eventRates.length;

    for(var j = 0; j < this.eventRates.length; j++) {
      if (this.eventRates[j] > avg/3) {
        var start = this.keyEvents[j].time - 2;
        var end = this.keyEvents[j+1].time + 2;
        this.highRateTimes.push([start, end]);
      }
    }
  }

  mergeTimeRanges() {
    var i = 0;
    var j = 1;
    var tmp = [this.highRateTimes[i]];
    while (j < this.highRateTimes.length) {
      var rangeA = tmp[i];
      var rangeB = this.highRateTimes[j];
      if (this.timesOverlap(rangeA, rangeB)) {
        tmp[i][0] = Math.min(rangeA[0], rangeB[0]);
        tmp[i][1] = Math.max(rangeA[1], rangeB[1]);
        j++;
      } else {
        tmp.push(rangeB);
        i++;
        j++;
      }
    }
    this.highlights = tmp;
  }

  mapToStreamTimestamps(demoGameStart, streamGameStart) {
    for (var i = 0; i < this.highlights.length; i++) {
      var s = this.highlights[i][0] - demoGameStart + streamGameStart;
      var e = this.highlights[i][1] - demoGameStart + streamGameStart;
      this.highlights[i][0] = this.secondsToTimestamp(s);
      this.highlights[i][1] = this.secondsToTimestamp(e);
    }
    console.log(this.highlights);
  }

  secondsToTimestamp(seconds) {
    var hours = Math.floor(seconds/3600);
    seconds = seconds%3600;
    var mins = Math.floor(seconds/60);
    seconds = Math.floor(seconds%60);
    return(this.formatTimestamp(hours,mins,seconds));
  }

  formatTimestamp(hours, mins, seconds) {
    hours = hours < 10 ? `0${hours}` : hours;
    mins = mins < 10 ? `0${mins}` : mins;
    seconds = seconds < 10 ? `0${seconds}` : seconds;
    return `${hours}h${mins}m${seconds}s`;
  }

  timesOverlap(timeA, timeB) {
    var [startA, endA] = timeA;
    var [startB, endB] = timeB;
    return ((startB <= endA) || (endA >= startB));
  }

  // for debugging only
  plotAllEvents() {
    var g = [];
    var j = 0;
    var eventCount = 0;
    for (var i = Math.floor(this.startTime); i < Math.floor(this.endTime); i++) {
      if (i == Math.floor(this.keyEvents[j].time)) {
        eventCount++;
        j = j < this.keyEvents.length - 1? j + 1 : j;
      }
      g.push(eventCount);
    }
    console.log(asciichart.plot(g));
  }

  plotHighRates() {
    var g = [];
    var j = 0;
    var rate = 0;
    for (var i = Math.floor(this.startTime); i < Math.floor(this.endTime); i++) {
      if (i == Math.floor(this.keyEvents[j].time)) {
        rate = this.eventRates[j] * 10;
        j = j < this.eventRates.length - 1? j + 1 : j;
      } else {
        rate = 0;
      }
      g.push(rate);
    }
    console.log(asciichart.plot(g));
  }

  plotHighlightTimes() {
    var g = [];
    var j = 0;
    var val = -1;
    var highlightTimes = [].concat.apply([], this.highlights);
    for (var i = Math.floor(this.startTime); i < Math.floor(this.endTime); i++) {
      if (i == Math.floor(highlightTimes[j])) {
        val *= -1;
        j = j < this.eventRates.length - 1? j + 1 : j;
      }
      g.push(val);
    }
    console.log(asciichart.plot(g));
  }
}

module.exports = Round;
