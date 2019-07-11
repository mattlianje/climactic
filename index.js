const inquirer = require('inquirer');

console.log(`Welcome to the Highlight Generator Tool`);
console.log();
console.log(`Please provide the following...`);
console.log(`======================================`);

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
        console.log(`Parse Running...`);
        var parseDemo = require('./demofile-parsing/parse_demo.js');
        parseDemo(inputURL,inputFile,inputStartTime);
    }
});