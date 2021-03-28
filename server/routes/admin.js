const auth = require('../middleware/auth');
const Event = require("../models/event")
const express = require("express");

const router = express.Router();

// @route   GET /admin
// @desc    Admin homepage
// @access  Admin
router.get("/admin", auth(['admin']), async (req, res) => {
    Event.findAll({}, {raw: true}).then(events => {
        // events will be an array of all Event instances
        console.log(events)
        res.json({ message: "Welcome to Admin Page!", events: events});
    })
    
});

// @route   POST /create_event
// @desc    Create event by Admin
// @access  Admin
router.post("/create_event", auth(['admin']),async (req, res)=> {
    const {event_name, disaster_type, severity, location, event_date, zipcode, items}=req.body;

    const alreadyExistsEvent=await Event.findOne({where: {event_name}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsEvent) {
        return res.json({message: "Event already exists!"});}

    const newEvent=new Event({event_name, disaster_type, severity, location, event_date, zipcode, items});
    const savedEvent=await newEvent.save().catch((err)=> {
        console.log("Error: ", err);
        res.json({error: "Cannot create event at the moment!"}); });

    if (savedEvent) res.json({message: "Event Created!"}); })

module.exports = router;