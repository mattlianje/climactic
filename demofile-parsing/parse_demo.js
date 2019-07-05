const fs = require("fs");
const demofile = require("demofile");
const path = require("path");
const Round = require('./Round.js');

const demPath = "/Users/tylerlam/Downloads/test.dem"; //add the filepath here

fs.readFile(path.resolve(demPath), (err, buffer) => {
  const demoFile = new demofile.DemoFile();
  var rounds = [];

  // parse start of the round
  demoFile.gameEvents.on("round_start", e => {
    rounds.push(new Round(demoFile.currentTime));
  });

  // parse end of the round
  var roundIndex = 0;
  demoFile.gameEvents.on("round_end", e => {
    var r = rounds[roundIndex];
    r.endTime = demoFile.currentTime;
    r.sortKeyEvents();
    r.calculateEventRates();
    r.getHighRateTimes();
    r.mergeTimeRanges();
    roundIndex++;
  });

  // parse deaths 
  demoFile.gameEvents.on("player_death", e => {
    deathEvent = { time: demoFile.currentTime, type: "player_death" };
    rounds[roundIndex].pushKeyEvent(deathEvent);
  });

  // parse bomb_defuses
  demoFile.gameEvents.on("bomb_defused", e => {
    bombDefuseEvent = { time: demoFile.currentTime, type: "bomb_defused" };
    rounds[roundIndex].pushKeyEvent(bombDefuseEvent);
  });

  // parse bomb_planted
  demoFile.gameEvents.on("bomb_planted", e => {
    bombPlantEvent = { time: demoFile.currentTime, type: "bomb_planted" };
    rounds[roundIndex].pushKeyEvent(bombPlantEvent);
  });

  demoFile.parse(buffer);
});
