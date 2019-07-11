const fs = require("fs");
const demofile = require("demofile");
const path = require("path");
const Round = require('./Round.js');

const DEBUG = false; // If you want to log stuff set this to true :))) 
const demPath = "/Users/tylerlam/Desktop/demfiles/ence-vs-astralis-m2-inferno.dem";
const streamGameStart = 595; // specific to the stream chosen. Must set this before running
var demoGameStart = null;

// maps seconds time of demofile to timestamp of video
function secondsToTimestamp(seconds, demoStart, streamStart) {
  demoStart = demoStart || 0;
  seconds = seconds - demoStart + streamStart;
  var hours = Math.floor(seconds/3600);
  seconds = seconds%3600;
  var mins = Math.floor(seconds/60);
  seconds = Math.floor(seconds%60);
  hours = hours < 10 ? `0${hours}` : hours;
  mins = mins < 10 ? `0${mins}` : mins;
  seconds = seconds < 10 ? `0${seconds}` : seconds;
  return `${hours}h${mins}m${seconds}s`;
}


fs.readFile(path.resolve(demPath), (err, buffer) => {
  const demoFile = new demofile.DemoFile();
  const rounds = [];
  var roundEvents = [];
  var roundLatestStart = 0;
  var roundOn = false;
  var roundIndex = 0;

  // parse start of the round
  demoFile.gameEvents.on("round_start", e => {
    roundOn = true;
    roundEvents = [];
    var t = demoFile.currentTime;
    roundLatestStart = t;
    // log round start
    console.log(`round ${roundIndex} started ${secondsToTimestamp(t, demoGameStart, streamGameStart)}`);

    if (DEBUG) {
      console.log(t);
    }
  });

  // parse end of the round
  demoFile.gameEvents.on("round_end", e => {
    if(roundOn == true){
      roundOn = false;
      var t = demoFile.currentTime;
      var round = new Round(roundLatestStart, t, roundEvents);
      rounds.push(round);
      // set the demo file game start to start time of round 1
      demoGameStart = demoGameStart == null? roundLatestStart : demoGameStart;
      // generate highlights for the round
      round.sortKeyEvents();
      round.calculateEventRates();
      round.getHighRateTimes();
      round.mergeTimeRanges();
      console.log(round.getStreamTimestamps(demoGameStart, streamGameStart));
      // reset roundEvents 
      roundEvents = [];
      // log round end
      console.log(`round ${roundIndex} ended ${secondsToTimestamp(t, demoGameStart, streamGameStart)}`);
      if (DEBUG) {
        round.plotAllEvents();
        round.plotHighRates();
        round.plotHighlightTimes();
        console.log(`set demoGameStart to: ${demoGameStart}`);
      }
      roundIndex++;
    }
  });

  demoFile.gameEvents.on("player_death", e => {
    var t = demoFile.currentTime - 20;
    if(roundOn == true){
      deathEvent = { time: t, type: "player_death" };
      roundEvents.push(deathEvent);
    }
    
    if (DEBUG) {
      const victim = demoFile.entities.getByUserId(e.userid);
      const victimName = victim ? victim.name : "unnamed";
      const attacker = demoFile.entities.getByUserId(e.attacker);
      const attackerName = attacker ? attacker.name : "unnamed";
      const headshotText = e.headshot ? " HS" : "";
      console.log(`${attackerName} [${e.weapon}${headshotText}] ${victimName} -> ${secondsToTimestamp(t, demoGameStart, streamGameStart)}`);
    }

  });

  // parse bomb_defuses
  demoFile.gameEvents.on("bomb_defused", e => {
    var t = demoFile.currentTime - 20;
    if(roundOn == true){
      bombDefuseEvent = { time: demoFile.currentTime, type: "bomb_defused" };
      roundEvents.push(bombDefuseEvent);
    }
    if (DEBUG) {
      console.log(`Bomb defused -> ${secondsToTimestamp(t, demoGameStart, streamGameStart)}`);
    }
  });

  // parse bomb_planted
  demoFile.gameEvents.on("bomb_planted", e => {
    var t = demoFile.currentTime - 20;
    if (roundOn == true) {
      bombPlantEvent = { time: demoFile.currentTime, type: "bomb_planted" };
      roundEvents.push(bombPlantEvent);
    }
    if (DEBUG) {
      console.log(`Bomb planted -> ${secondsToTimestamp(t, demoGameStart, streamGameStart)}`);
    }
  });

  demoFile.parse(buffer);
});
