const app = require('./server')
const PORT = process.env.PORT || 5000; // look for default port else set to 5000 for local

app.listen(PORT, ()=>{
    console.log(`Server started on PORT ${PORT}`);
});