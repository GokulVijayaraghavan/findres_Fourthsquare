const express = require('express');
const opn = require('opn');

const app = express();

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:3000`);
  opn(`http://localhost:3000`);
});