const express = require('express');
const app = express();
const port = 3003;

let urlDB = {}; // used to store the url mapping obj in memory

function generateId() {
  // generate a random 6 digit ID for url mapping
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  for (let i = 0; i < 6; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function isValidURL(url) {
  // verify the validity of the long url
  const urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
  return urlPattern.test(url);
}

app.use(express.json());

app.get('/', (req, res) => {
  const shortUrls = `http://localhost:3003/${Object.keys(urlDB)}`; // get all the short ID
  res.status(200).json(shortUrls); // return shortID
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

app.post('/shorten', (req, res) => {
  const { url } = req.body; // get url from req body
  if (url) {
    if (isValidURL(url)){
      const id = generateId();
      urlDB[id] = url; // map short id with url, stored in the memory
      console.log(urlDB);
      res.status(201).json({ id: id, shortUrl: `http://localhost:3003/${id}` });
    }
  } else {
    res.status(400).json({ error: 'No URL provided' });
  }
});

app.get('/:id', (req, res) => {
  // redirect to the url via corresponding shorten ID
  const { id } = req.params; 
  const url = urlDB[id]; 
  if (url) {
    res.redirect(url); 
  } else {
    res.status(404).send('Not found'); 
  }
});

app.put('/:id', (req, res) => {
  const { id } = req.params; // get short ID from url
  const { url } = req.body; // get New url from req

  if (urlDB[id]) { // check if the short ID exists
    // check if New url provided
    if (url) {
      if (isValidURL(url)){
        urlDB[id] = url; // update the new url to the existing short ID
        res.status(200).send(`URL for ${id} updated to ${url}`);
      }
    } else {
      res.status(400).send('No URL provided');
    }
  } else {
    res.status(404).send('ID not found');
  }
});

app.delete('/:id', (req, res) => {
  const { id } = req.params; // get short id from req url

  if (urlDB[id]) {
    delete urlDB[id]; // delete corresponding url
    res.status(204).send(); 
  } else {
    res.status(404).send('ID not found'); 
  }
});

