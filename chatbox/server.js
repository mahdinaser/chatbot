//@ts-check
"use strict";
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var fs = require('fs')
var filename = 'data/chatbox.txt';
//var fs = require(fs);
var htmlPath = __dirname + '/viewcontrol';
app.use(express.static(htmlPath));
app.use(bodyParser.json());

app.set('views', htmlPath);
app.set('view engine', 'html');

var index = require('./myroutes/index.js');

app.get('/chatbox/sendquestion/:customer_question', function (req, res) {
    // var readFileCallback = function (err, data) {
    //     if (err) {
    //         res.status(500).send({ message: 'Error in reading the file' });
    //         return console.log(err);
    //     }
    //     console.log(data);
    //     res.status(200).send(data);
    // };
    // fs.readFile(filename, 'utf8', readFileCallback);
    let user_id = 1    
    let customer_question = req.params.customer_question;
    console.log('/: I received a GET request. /chatbox/:customer_question=', customer_question, 'user_id=', user_id);
    console.log()
    index.sendquestion(res, user_id, customer_question);
});
// app.post('/', function (req, res) {
//     console.log('/: I received a POST request');
//     console.log(req.body);
//     //res.end({url:'/'});

//     var readFileCallback = function (err, data) {
//         if (err) {
//             res.status(500).send({ message: 'Error in reading the file' });
//             return console.log(err);
//         }
//         console.log(data);
//         data += '\n' + req.body.data;
//         fs.writeFile(filename, data, (err) => {
//             // throws an error, you could also catch it here
//             if (err) throw err;
//             res.status(201).send(data);
//             //res.json(data);
//         });
//     };
//     //read file then write the post json data
//     fs.readFile(filename, 'utf8', readFileCallback);
// });
var port = 9001;
app.listen(port);
console.log("Server running on port (", port,
    "). Open the following link to start the server: \n http://localhost:" + port);