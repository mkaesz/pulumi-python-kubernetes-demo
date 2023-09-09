'use strict';

const express = require('express');
require('dotenv').config();

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
const value_from_pulumi_config = process.env.PULUMI_CFG_VALUE

app.get('/', (req, res) => {
  res.send(`Hello World ${value_from_pulumi_config}`);
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
