const fs = require("fs");
const demofile = require("demofile");
const path = require("path");
const Round = require("./Round.js");
const demPath = "C:/Users/eldri/Documents/GitHub/Local_Files/exec-vs-noname-mirage(multiple-round-start).dem"; //add the filepath here

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
    roundLatestStart = demoFile.currentTime;
    // CONSOLE LOGGING - ONLY NECESSARY FOR TEST PURPOSES
    console.log(`round ${roundIndex} started ${demoFile.currentTime}`);
  });

  // parse end of the round
  demoFile.gameEvents.on("round_end", e => {
    if(roundOn == true){
      roundOn == false;
      rounds.push(new Round(roundLatestStart, demoFile.endTime, roundEvents));
      var r = rounds[roundIndex];
      r.sortKeyEvents();
      r.calculateEventRates(roundIndex);
      r.getHighRateTimes();
      r.mergeTimeRanges();
      // r.mapToStreamTimestamps(gameStart);
      // r.plotAllEvents();
      // r.plotHighRates();
      roundEvents = [];
      console.log(`round ${roundIndex} ended ${demoFile.currentTime}`);
      roundIndex++;
    }

    // CONSOLE LOGGING - ONLY NECESSARY FOR TEST PURPOSES
    // console.log(`round ${roundIndex} ended`);
    // roundIndex++;
  });

  demoFile.gameEvents.on("player_death", e => {
    if(roundOn == true){
      deathEvent = { time: demoFile.currentTime, type: "player_death" };
      roundEvents.push(deathEvent);
    }
    
    //CONSOLE LOGGING - ONLY NECESSARY FOR TEST PURPOSES
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
  });

  // parse bomb_defuses
  demoFile.gameEvents.on("bomb_defused", e => {
    if(roundOn == true){
      bombDefuseEvent = { time: demoFile.currentTime, type: "bomb_defused" };
      roundEvents.push(bombDefuseEvent);
    }
  });

  // parse bomb_planted
  demoFile.gameEvents.on("bomb_planted", e => {
    if(roundOn == true){
      bombPlantEvent = { time: demoFile.currentTime, type: "bomb_planted" };
      roundEvents.push(bombPlantEvent);
    }
  });

  demoFile.parse(buffer);
});
