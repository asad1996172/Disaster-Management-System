const auth = require('../middleware/auth');
const Event = require("../models/event")
const express = require("express");

const router = express.Router();

// @route   GET /admin
// @desc    Admin homepage
// @access  Admin
router.get("/admin", auth(['admin']), async (req, res) => {
    res.json({ message: "Welcome to Admin Page!"});
});

// @route   POST /create_event
// @desc    Create event by Admin
// @access  Admin
router.post("/create_event", auth(['admin']), async (req, res)=> {
    const {name, disaster_type, location, zipcode, severity, items, event_date}=req.body;

    const alreadyExistsEvent=await Event.findOne({where: {name}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsEvent) {
        return res.json({message: "Event already exists!"});}

    

    const newEvent=new Event({});
    const savedEvent=await newEvent.save(name, disaster_type, severity, location, event_date, zipcode, items).catch((err)=> {
        console.log("Error: ", err);
        res.json({error: "Cannot create event!"}); });

    if (savedEvent) res.json({message: "Event Created!"}); })

module.exports = router;