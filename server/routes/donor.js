const auth = require('../middleware/auth');
const Event = require("../models/event");
const Request = require("../models/request");
const express = require("express");

const router = express.Router();

router.get("/donor", auth(['donor']), async (req, res) => {
    
    Request.findAll({}, {raw: true}).then(requests => {
        // events will be an array of all Event instances
        console.log(requests)
        res.json({ message: "Welcome to Donor Page!", requests: requests});
    });
});

router.post("/make_donation", auth(['donor']), async (req, res) => {
    const {event_name, donor_email, recipient_email, items}=req.body;

    const alreadyExistsRequest=await Request.findOne({where: {event_name: event_name, email: recipient_email}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsRequest) {
        alreadyExistsRequest.update({
            item_quantities: items
        }).then(function() { 
            return res.json({message: "Donation Successfull!"});
        })

    }
});

module.exports = router;