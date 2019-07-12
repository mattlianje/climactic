const inquirer = require('inquirer');

console.log(`Welcome to the Highlight Generator Tool`);
console.log();
var testURL = "https://www.twitch.tv/videos/449439967"; // Change according to Testing needs
var testFilePath = "C:/Users/eldri/Documents/GitHub/Local_Files/heroic-vs-ence-mirage.dem"; // Change according to Testing needs
var testStartTime = 2000; // Change according to Testing needs

const TESTING = false; //Turn this on to skip prompts when testing

if(TESTING){ 
    console.log(`Parse Running...`);
    console.log();
    var parseDemo = require('./parse_demo.js');
    parseDemo(testURL,testFilePath,testStartTime);
}
else {
    console.log(`Please provide the following...`);
    console.log(`======================================`);
    console.log();
    var questions = [
        {
            type: 'editor',
            name: 'inputURL',
            message: "Twitch Stream URL",
        },
        {
            type: 'editor',
            name: 'inputFile',
            message: "Exact path to Demo File",
        },
        {
            type: 'input',
            name: 'inputStartTime',
            message: "The time at which your CS:GO match starts (in seconds):",
        },
        {
            type: 'list',
            name: 'startPrompt',
            message: "Run?",
            choices: ["Yes", "No"],
        }
    ]
    
    inquirer.prompt(questions).then(answers => {
        inputURL = answers['inputURL'];
        inputFile = answers['inputFile'];
        inputStartTime = answers['inputStartTime'];
        if (answers['startPrompt'] == "No") {
            console.log(`======================================`);
            console.log(`Lets try this again.`);
            getUserInput();
        } else {
            console.log(`======================================`);
            console.log(`You entered: ${inputURL}, ${inputFile}, ${inputStartTime}`);
            console.log();
            console.log(`Parse Running...`);
            console.log();
            var parseDemo = require('./parse_demo.js');
            parseDemo(inputURL,inputFile,inputStartTime);
        }
    });
}