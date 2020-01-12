const { DEBUG } = require('./constants');

const Logger = {
  debug(msg) {
    if (DEBUG) {
      console.log(msg);
    }
  },
  log(msg) {
    console.log(msg);
  }
}

module.exports = Logger;
