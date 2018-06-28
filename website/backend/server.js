const Pusher = require('pusher');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const imgdir = '../public/comparisons';
const app = express();

app.use(cors());
//app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));
app.set('PORT', process.env.PORT || 5000);

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
db.query('SELECT * FROM faces', function(err, result){
  if(err){
    console.error(err);
  } else {
    console.log(result.rows);
    console.log("DB confirmed connected :)");
  }
});


//initializing pusher client
const pusher = new Pusher({
  appId: '549821',
  key: 'ac944354925fa2b30b7e',
  secret: 'db94ac25dcc90c638935',
  cluster: 'ap1',
  encrypted: true
});


//test route
app.post('/message', (req, res) => {
  const payload = req.body;
  pusher.trigger('imgrec', 'test', payload);
  res.send(payload)
});

//Create new faces
app.post('/create', (req, res) => {
  //contains b64 encoded image data
  const payload = req.body.body;
  const facetoken = req.body.facetoken;
  const name = req.body.name;
  
  console.log("saving to image to local file")
  //saving to local face archive
  fs.writeFile("../src/faces/"+facetoken+".png",payload,'base64',function(err){
    if(err) {
      console.log(err)
    }
  })
  
  //update database
  db.query('INSERT INTO faces VALUES (\''+name+'\',\''+facetoken+'\')', function(err, result){
    if(err){
      console.log(err)
    }
  });

  res.send("added to local db OK")
});

app.post('/viewall', (req, res) => {
  var query = "select * from faces"
  db.query(query, function(err, result){
    if(err){
      console.log(err)
    } else {
      if(result.rows.length > 0){
        res.json(result.rows)
      }
    }
  });
});

app.post('/compare', (req, res)=> {
  
  const facetoken= req.body.comparison_token
  const imagedata = req.body.comparison_image

  //remove all files in comparisons folder
  fs.readdir(imgdir, (err, files) => {
    if(err){
      console.log(err)
    }
    for(const file of files){
      fs.unlink(path.join(imgdir, file), err => {
        if (err) throw err;
      });
    }
  })

  //add file to local comparisons folder
  fs.writeFile(imgdir+"/"+facetoken+".png",imagedata,'base64',function(err){
    if(err) {
      console.log(err)
    }
  })

  const payload = {
    'comparison_token': facetoken,  
    'user_id': req.body.user_id,
    'face_token': req.body.face_token,
    'confidence': req.body.confidence
  }

  pusher.trigger('imgrec', 'comparison', payload)
  res.send("YES OK VERY GOOD")
});


app.listen(app.get('PORT'), () => 
  console.log('Listening at ' + app.get('PORT')))

