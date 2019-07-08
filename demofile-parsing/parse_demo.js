const fs = require("fs");
const demofile = require("demofile");
const path = require("path");
const Round = require("./Round.js");

fs.readFile(path.resolve("/Users/tylerlam/Downloads/test.dem"), (err, buffer) => {
  const demoFile = new demofile.DemoFile();
  const rounds = [];
  var round_i = false;

  // parse start of the round
  demoFile.gameEvents.on("round_start", e => {
    if(round_i == true){
      rounds.pop();
    }
    round_i = true;
    rounds.push(new Round(demoFile.currentTime));
    
    // CONSOLE LOGGING - ONLY NECESSARY FOR TEST PURPOSES
    // console.log(`round ${roundIndex} started ${demoFile.currentTime}`);
  });

  // parse end of the round
  var roundIndex = 0;
  demoFile.gameEvents.on("round_end", e => {
    if(round_i == true){
      var r = rounds[roundIndex];
      r.endTime = demoFile.currentTime;
      r.sortKeyEvents();
      r.calculateEventRates(roundIndex);
      r.getHighRateTimes();
      r.mergeTimeRanges();
      // r.mapToStreamTimestamps(gameStart);
      // r.plotAllEvents();
      // r.plotHighRates();

      // CONSOLE LOGGING - ONLY NECESSARY FOR TEST PURPOSES
      // console.log(`round ${roundIndex} ended`);
      round_i == false;
      roundIndex++;
    }
  });

  demoFile.gameEvents.on("player_death", e => {
    if(round_i == true){
      deathEvent = { time: demoFile.currentTime, type: "player_death" };
      rounds[roundIndex].pushKeyEvent(deathEvent);

      // CONSOLE LOGGING - ONLY NECESSARY FOR TEST PURPOSES
      // const victim = demoFile.entities.getByUserId(e.userid);
      // const victimName = victim ? victim.name : "unnamed";

      // // Attacker may have disconnected so be aware.
      // // e.g. attacker could have thrown a grenade, disconnected, then that grenade
      // // killed another player.
      // const attacker = demoFile.entities.getByUserId(e.attacker);
      // const attackerName = attacker ? attacker.name : "unnamed";

      // const headshotText = e.headshot ? " HS" : "";
      // const currentTime = demoFile.currentTime;
      // console.log(`${attackerName} [${e.weapon}${headshotText}] ${victimName} -> time: ${currentTime}`);
    }
  });

  // parse bomb_defuses
  demoFile.gameEvents.on("bomb_defused", e => {
    if(round_i == true){
      bombDefuseEvent = { time: demoFile.currentTime, type: "bomb_defused" };
      rounds[roundIndex].pushKeyEvent(bombDefuseEvent);
    }
  });

  // parse bomb_planted
  demoFile.gameEvents.on("bomb_planted", e => {
    if(round_i == true){
      bombPlantEvent = { time: demoFile.currentTime, type: "bomb_planted" };
      rounds[roundIndex].pushKeyEvent(bombPlantEvent);
    }
  });

  demoFile.parse(buffer);
});
