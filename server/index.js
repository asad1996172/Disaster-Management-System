const express = require('express');
const connectDB = require('./config/db');

const app = express();

// Connect and create databse
connectDB(); 

app.get('/', (req, res)=>{
    res.send('API Running');
});

const PORT = process.env.PORT || 5000; // look for default port else set to 5000 for local

app.listen(PORT, ()=>{
    console.log(`Server started on PORT ${PORT}`);
});