var express = require('express');
var app = express();
app.use(express.json());       // to support JSON-encoded bodies

/*
var loginRouter = require('./create.js');
app.use('/', createRouter);

//create entry in projectsownership
var createProjectRouter = require('./compare.js');
app.use('/', compareRouter);
*/

//connecting to db
var pg = require("pg");
var db = new pg.Client({user: 'postgres', password: 'Linde123', database: 'postgres', host: 'localhost'});
var response = "";
db.connect(function(err) {
	if(err) {
		return console.error('could not connect to postgres', err);
	}
});

//Testing db connection
db.query('SELECT * FROM img', function(err, result){
	if(err){
		console.error(err);
	} else {
		console.log("retrieved is ",result.rows[0]);
		console.log("DB confirmed connected :)");
	}
});

module.exports = app;

//default port set to 8080
app.set('port', process.env.PORT || 8080);
app.listen(app.get('port'));
