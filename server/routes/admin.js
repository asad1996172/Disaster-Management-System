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
router.post("/create_event", auth(['admin']), async (req, res)=> {
    const {event_name, disaster_type, severity, location, event_date, zipcode, items}=req.body;

    /* istanbul ignore next */
    const alreadyExistsEvent=await Event.findOne({where: {event_name}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );


    if (alreadyExistsEvent) {
        /* istanbul ignore next */
        return res.json({message: "Event already exists!"});
    }

    const newEvent=new Event({event_name, disaster_type, severity, location, event_date, zipcode, items});
    /* istanbul ignore next */
    const savedEvent=await newEvent.save().catch((err)=> {
        console.log("Error: ", err);
        res.json({error: "Cannot create event at the moment!"}); });

    if (savedEvent) res.json({message: "Event Created!"}); })


// @route   POST /edit_event
// @desc    Edit event
// @access  Admin
router.post("/edit_event", auth(['admin']), async (req, res)=> {
    const { event_name, disaster_type, severity, location, event_date, zipcode, items }=req.body;

    let updateValues = { 
        event_name: event_name,
        disaster_type: disaster_type,
        severity: severity,
        location: location,
        event_date: event_date,
        zipcode: zipcode,
        items: items
    };
        Event.update(updateValues, { where: { event_name: event_name } }).then((result) => {
            // here your result is simply an array with number of affected rows
            console.log(result);
            return res.json({message: "Event Expired Successfully!"});
            // [ 1 ]
    });

})

    // @route   POST /expire_event
// @desc    Expire event
// @access  Admin
router.post("/expire_event", auth(['admin']), async (req, res)=> {
    const { event_name }=req.body;

    let updateValues = { expired: true };
        Event.update(updateValues, { where: { event_name: event_name } }).then((result) => {
            // here your result is simply an array with number of affected rows
            console.log(result);
            return res.json({message: "Event Expired Successfully!"});
            // [ 1 ]
    });

})

// @route   GET /get_event
// @desc    Get event
// @access  Admin
router.get("/get_event", auth(['admin']), async (req, res)=> {
    const { event_name }=req.body;
    const alreadyExistsEvent=await Event.findOne({where: {event_name}})
    if (alreadyExistsEvent) {
        return res.json({message: "Event deleted successfully", event_details: alreadyExistsEvent});
    }
    return res.json({message: "Event doesnot exist"});
})

    // @route   POST /delete_event
// @desc    Delete event
// @access  Public
router.post("/delete_event", async (req, res)=> {
    const { event_name }=req.body;

    const alreadyExistsEvent=await Event.findOne({where: {event_name}})
    if (alreadyExistsEvent) {
        await Event.destroy({where: {event_name}})
        return res.json({message: "Event deleted successfully"});
    }

    return res.json({message: "Event doesnot exist"});
})
module.exports = router;