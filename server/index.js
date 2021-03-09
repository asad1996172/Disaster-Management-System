require("dotenv").config();
require("./models/user");

const express = require('express');
const bodyParser = require("body-parser");
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Initialize middleware
const middlewares = require("./middlewares");
const api = require("./routes");

app.get('/', (req, res)=>{
    res.json({ status: 'API Running'});
});

// Define Routes
app.use("/api/v1", api);

app.use(middlewares.notFound);
app.use(middlewares.errorHandler);

const PORT = process.env.PORT || 5000; // look for default port else set to 5000 for local

app.listen(PORT, ()=>{
    console.log(`Server started on PORT ${PORT}`);
});