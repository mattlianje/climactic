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
    this.playerKills = {};
    this.firstKills = {};
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
    for (var i = 0; i+1 < this.keyEvents.length; i++) {
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

  getStreamTimestamps(demoGameStart, streamGameStart) {
    var result = [];
    for (var i = 0; i < this.highlights.length; i++) {
      var s = this.highlights[i][0] - demoGameStart + streamGameStart;
      var e = this.highlights[i][1] - demoGameStart + streamGameStart;
      result.push([this.secondsToTimestamp(s), this.secondsToTimestamp(e)]);
    }
    return result;
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

  getKills() {
    // Hardcode the max delta between 1st and 4th kills in a 4k for it to count as a highlight.
    var maxTimeFirst2Last = 30;

    for (var i = 0; i < this.keyEvents.length; i++) {

    //   // If the event is a player death add the killer to the array.
      if (this.keyEvents[i].type == 'player_death') {
        var killerName = this.keyEvents[i].attacker_name;

        // If the attacker name is in the array increment the kill count +1 an overwrite.
        if (killerName in this.playerKills) {
          var newPlayerKills = this.playerKills[killerName] + 1;
          this.playerKills[killerName] = newPlayerKills;

          if (newPlayerKills == 4) {
            // Delta of 4th kill time and first kill time.
            var firstKillTime = this.firstKills[killerName];

            if ((this.keyEvents[i].time - firstKillTime) <= maxTimeFirst2Last) {
              console.log('**ALERT** ' + killerName + ' got 4 kills within ' + maxTimeFirst2Last + ' seconds.');
            }
          }

          if (newPlayerKills == 5) {
            console.log('**ALERT** ' + killerName + ' got 5 kills.');
          }

        } else {
          // Get the timestamp of the first kill.
          var firstKillTime = this.keyEvents[i].time;
          // Add the first kill time to the 'dictionnary' of playerNames and first kill times for that round.
          this.firstKills[killerName] = firstKillTime;
          this.playerKills[killerName] = 1;
        }
      }
    }
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
