// USAGE: npm start *insert youtube vid*

const fetchVideoInfo = require('youtube-info');
const request = require('request');
var dbConnection = require('./secretsJS')

const args = process.argv.slice(2);
const youtubeUrl = args[0];
var TESTING = false;
if(args[1] == "log"){var TESTING = true;}

var mysql = require('mysql');
// CONNECT TO DB
if(TESTING){ // Localhost when testing
  var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    database: "climactic_test"
  });
}else{ // Prod DB
  var con = mysql.createConnection({
    host: dbConnection.host,
    user: dbConnection.username,
    password: dbConnection.password,
    database: dbConnection.database
  });
}
// -----------------------------

const getVideoId = (url) => {
  var videoId = null;
  if (url.includes("youtube")) {
    videoId = url.split("v=")[1];
    var ampersand = videoId.indexOf('&');
    if (ampersand != -1) {
      videoId = videoId.substring(0, ampersand);
    }
  }
  return videoId;
}

var videoId = null;
var videoDuration = null;

const getClipIntervals = (totalLength, clipLength, overlapLength) => {
  const intervals = [];
  var startTime = 0;
  var endTime = startTime + clipLength;
  while (endTime <= totalLength) {
    intervals.push([startTime, endTime]);
    startTime = endTime - overlapLength;
    endTime = startTime + clipLength;
  }
  if (endTime > totalLength) {
    intervals.push([startTime, totalLength]);
  }

  return intervals;
}

const formatRow = (youtubeUrl, start, end) => {
  return `('${ youtubeUrl }', ${ start }, ${ end })`;
}

const formatQueryString = (youtubeUrl, intervals) => {
  values = intervals.map( interval => formatRow(youtubeUrl, interval[0], interval[1]));
  query = `INSERT INTO labelled (url, start, end) VALUES ${values.join(", ")};`;
  return query
}

const sendtoDBUsingSQL = (sql) => {
  con.connect(function(err) {
    if (err) throw err;
    console.log("Connected to db");
    con.query(sql, function (err, result) {
      if (err) throw err;
    });
    con.end();
  });
}

const OVERLAP_TIME = 2;
const CLIP_LENGTH = 4; 

if (youtubeUrl) {
  console.log(youtubeUrl)
  videoId = getVideoId(youtubeUrl);
  fetchVideoInfo(videoId, (err, videoInfo) => {
    if (err) throw new Error(err);
    videoDuration = videoInfo.duration;
    console.log(videoDuration);
    const clipIntervals = getClipIntervals(videoDuration, CLIP_LENGTH, OVERLAP_TIME);
    query = formatQueryString(youtubeUrl, clipIntervals);
    sendtoDBUsingSQL(query);
    console.log(`${ clipIntervals.length } inserted into db`);
  });
} else {
  console.log(" USAGE: npm start *insert youtube vid url*");
}
