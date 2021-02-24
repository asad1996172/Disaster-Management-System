const mysql = require('mysql');
// Useful tips: Use try catch with async await

const connectDB = async() => {
    // Create connection
    const db = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: ''
    });
    
    // Make Connection
    try{
        await db.connect();
        console.log('MySQL Connected ...')
    } catch (err){
        console.error(err.message);
        process.exit(1); // exit process with failure
    }

    // Create Database
    try {
        let create_db = 'CREATE DATABASE IF NOT EXISTS dams';
        await db.query(create_db);
    } catch (err) {
        console.error(err.message);
        process.exit(1); // exit process with failure
    }
}

module.exports = connectDB;
