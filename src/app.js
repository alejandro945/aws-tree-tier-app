const mysql = require('mysql');
const express = require('express');
require('dotenv').config();
const app = express();
const port = process.env.PORT || 80;

const connection = mysql.createConnection({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.USER || 'myuser',
  password: process.env.PASSWORD || 'mypassword',
  database: process.env.DATABASE || 'mydatabase',
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL database!');
});

/**
 * Entry point for the application.
 */
app.get('/', (_, res) => {
  res.send('Hello World!');
});

/**
 * Test endpoint for test purposes.
 */
app.get('/test', (_, res) => {
  res.send('Hello Test!');
});

app.listen(port, () => console.log(`Listening on port ${port}!`));

exports.connection = connection;