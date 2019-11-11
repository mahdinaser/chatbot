"use restrict";
//@ts-check
var fs = require('fs');
var child_process = require('child_process');

module.exports = {



    //post(add) the student assitant's time log in/out if the user is authorized to run this program
    sendquestion: function (res, user_id, customer_question) {
        console.log('index.js: sendquestion()');
        currentPath = __dirname;
        const pyProgram = currentPath + '\\python\\chatbox_service.py';
        console.log('index.js: sendquestion(), pyProgram', pyProgram);


        var spawn = child_process.spawn,
            py = spawn('python', [pyProgram]),
            //[term,filename,path,connString]

            input = [user_id, customer_question],

            printString = '';

        py.stdout.on('data', function (data) {
            printString += data.toString();
        });
        py.stdout.on('end', function () {
            console.log('End message=', printString);
            // var pRet = `<br><br><br><a href="../../index.html"> Return to the page</a>`
            var end_line = "##end session##";
            if (printString.includes(end_line)) {
                // res.send(printString.replace(end_line, "").replace("\n\n", ""));
                res.send(printString.replace(end_line, ""));
            } else {
                return res.status(400).send('<b color=red>The program does not ends correctly</b>'+printString);
            }

        });
        py.stdin.write(JSON.stringify(input));
        py.stdin.end();



    }, //sendquestion: function

};
