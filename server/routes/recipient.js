const auth = require('../middleware/auth');
const Event = require("../models/event");
const Request = require("../models/request");
const express = require("express");

const router = express.Router();

router.get("/recipient", auth(['recipient']), async (req, res) => {
    Event.findAll({}, {raw: true}).then(events => {
        // events will be an array of all Event instances
        console.log(events)
        res.json({ message: "Welcome to Recipient Page!", events: events});
    });
});


router.post("/request_resources", auth(['recipient']), async (req, res) => {
    const {event_name, email, item_quantities}=req.body;

    const alreadyExistsRequest=await Request.findOne({where: {event_name: event_name, email: email}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsRequest) {
        return res.json({message: "Request already exists!"});}

    const newRequest=new Request({event_name, email, item_quantities});
    const savedRequest=await newRequest.save().catch((err)=> {
        console.log("Error: ", err);
        res.json({error: "Cannot save request at the moment!"}); });

    if (savedRequest) res.json({message: "Request Created!"});
});

module.exports = router;