const Pusher = require('pusher');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

const pusher = new Pusher({
  appId: '549821',
  key: 'ac944354925fa2b30b7e',
  secret: 'db94ac25dcc90c638935',
  cluster: 'ap1',
  encrypted: true
});
app.set('PORT', process.env.PORT || 5000);

app.post('/message', (req, res) => {
  const payload = req.body;
  pusher.trigger('imgrec', 'message', payload);
  res.send(payload)
});

app.post('/handsup', (req, res)=> {
  const payload = req.body;
  pusher.trigger('imgrec', 'message', payload);
  res.send(payload)
});

app.listen(app.get('PORT'), () => 
  console.log('Listening at ' + app.get('PORT')))