const fs = require("fs");
const demofile = require("demofile");
const path = require("path");

fs.readFile(path.resolve("/Users/tylerlam/Downloads/test.dem"), (err, buffer) => {
  const demoFile = new demofile.DemoFile();

  demoFile.gameEvents.on("player_death", e => {
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
  });

  demoFile.parse(buffer);
});
