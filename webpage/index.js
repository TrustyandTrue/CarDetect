const express = require('express');
const bodyParser = require('body-parser');
const request = require('request')
const formidable = require('formidable')
const fs = require('fs')
const PythonShell = require('python-shell')
const exec = require('child_process').exec

const app = express();

app.use(express.static('public'));
app.use(express.urlencoded({extended: true}));
app.set('view engine', 'ejs')

process.env.PWD = process.cwd()
app.use(express.static(process.env.PWD + '/uploads'));

app.get('/', function (req, res) {
   res.render('index', {uploadedImage: null, prediction1: null, prediction2: null, prediction3: null, error: null});
})

app.listen(8080, function () {
  console.log('Example app listening on port 8080!');
})

app.post('/', function (req, res) {
  res.render('index');
})

var itmp = null;
var pathForScript = null;

app.post('/upload', function (req, res) {

var form = new formidable.IncomingForm();
form.parse(req, function(err, fields, files) {
	var path = files.filetoupload.path;
	console.log(files);
	
	fs.readFile(path, function(err, data) {
		if(!path){
			console.log("No path given");
			res.redirect("/")
		}
		else {
			console.log("Path given")
			console.log(data);
			var newPath = __dirname + "/uploads/" + files.filetoupload.name;
			pathForScript = newPath;
			console.log(newPath);
			fs.writeFile(newPath, data, function(err) {
				console.log(err);
			});
			itmp = "/" + files.filetoupload.name;
			var arg = "--image " + pathForScript;
			res.render('index', {uploadedImage: itmp,  prediction1: "Waiting for prediction", prediction2: null, prediction3: null, error: null});
		}
	});
	
	

})
});

app.post('/predict', function (req, res) {
    var spawn = require("child_process").spawn;
	var arg = "--image " + pathForScript;
	console.log("arg: " + arg); 
    var process = exec('python' + ' ../model_execution/classifier_dummy.py '  + arg, null, (e, data) => {
//    var process = exec('python' + ' ../model_execution/classify.py '  + arg, null, (e, data) => {
    var n = data.split("\n");
    var first = n[n.length-4];
    var second = n[n.length-3];
    var third = n[n.length-2];
	console.log("First: " + first);
	console.log("Second: " + second);
	console.log("Third: " + third);
        
	res.render('index', {uploadedImage: itmp, prediction1: first, prediction2: second, prediction3: third, error: null});
    });
});


