const fs = require("fs");
const demofile = require("demofile");
const path = require("path");
const Round = require("./Round.js");

const demPath = "vitality-vs-nip-dust2.dem"; //add the filepath here
const gameStart = 13301; 

fs.readFile(path.resolve(demPath), (err, buffer) => {
  const demoFile = new demofile.DemoFile();
  const rounds = [];
  // parse start of the round
  demoFile.gameEvents.on("round_start", e => {
    console.log(`round ${roundIndex} started ${demoFile.currentTime}`);
    rounds.push(new Round(demoFile.currentTime));
    // console.log(rounds.length);
  });

  // parse end of the round
  var roundIndex = 0;
  demoFile.gameEvents.on("round_end", e => {
    var r = rounds[roundIndex];
    r.endTime = demoFile.currentTime;
    r.sortKeyEvents();
    // r.calculateEventRates();
    // r.getHighRateTimes();
    // r.mergeTimeRanges();
    // r.mapToStreamTimestamps(gameStart);
    // r.plotAllEvents();
    // r.plotHighRates();
    console.log(`round ${roundIndex} ended`);
    roundIndex++;
  });

// Ignores anything before the first round stars

  demoFile.gameEvents.on("player_death", e => {
    // Ignores all the game events before the start of round 0.
    if (rounds.length > 0) {
      const victim = demoFile.entities.getByUserId(e.userid);
      const victimName = victim ? victim.name : "unnamed";

      // Attacker may have disconnected so be aware.
      // e.g. attacker could have thrown a grenade, disconnected, then that grenade
      // killed another player.
      const attacker = demoFile.entities.getByUserId(e.attacker);
      const attackerName = attacker ? attacker.name : "unnamed";

      const headshotText = e.headshot ? " HS" : "";
      const currentTime = demoFile.currentTime;

      console.log(`${attackerName} [${e.weapon}${headshotText}] ${victimName} -> time: ${currentTime}`);
      deathEvent = { time: demoFile.currentTime, type: "player_death" };
      rounds[roundIndex].pushKeyEvent(deathEvent);
    }
  });

  // parse bomb_defuses
  demoFile.gameEvents.on("bomb_defused", e => {
    if(rounds.length > 0) {
      bombDefuseEvent = { time: demoFile.currentTime, type: "bomb_defused" };
      rounds[roundIndex].pushKeyEvent(bombDefuseEvent);
    }
  });

  // parse bomb_planted
  demoFile.gameEvents.on("bomb_planted", e => {
    if (rounds.length > 0) {
      bombPlantEvent = { time: demoFile.currentTime, type: "bomb_planted" };
      rounds[roundIndex].pushKeyEvent(bombPlantEvent);
    }
  });

  demoFile.parse(buffer);
});
