const inquirer = require('inquirer');
const { TEST_URL, TEST_FILE_PATH, TEST_START_TIME, TESTING } = require('./constants');

console.log(`Welcome to the Highlight Generator Tool`);


if(TESTING){ 
    console.log(`Parse Running...`);
    console.log();
    var parseDemo = require('./parse_demo.js');
    parseDemo(TEST_URL, TEST_FILE_PATH, TEST_START_TIME);
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