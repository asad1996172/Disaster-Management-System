const express = require('express');
const connectDB = require('./config/db');

const app = express();

// Connect databse
connectDB(); 

// Initialize middleware
app.use(express.json({ extended: false }));

app.get('/', (req, res)=>{
    res.send('API Running');
});

// Define Routes
const PORT = process.env.PORT || 5000; // look for default port else set to 5000 for local

app.listen(PORT, ()=>{
    console.log(`Server started on PORT ${PORT}`);
});
