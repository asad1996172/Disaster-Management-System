const mongoose = require('mongoose');
require('dotenv').config()

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost/mern-starter';
// Useful tips: Use try catch with async await

const connectDB = async() => {
    try{
        await mongoose.connect(MONGODB_URI, {
          useNewUrlParser: true,
          useUnifiedTopology: true,
          useCreateIndex: true,
          useFindAndModify: false
        });
        console.log('MongoDB connected ...')
    } catch (err){
        console.error(err.message);
        process.exit(1); // exit process with failure
    }
}

module.exports = connectDB;