const auth = require('../middleware/auth');
const Request = require("../models/request");
const Pledge = require("../models/pledge");
const express = require("express");

const router = express.Router();

router.get("/donor", auth(['donor', 'admin']), async (req, res) => {
    
    Request.findAll({}, {raw: true}).then(requests => {
        // events will be an array of all Event instances
        console.log(requests)
        res.json({ message: "Welcome to Donor Page!", requests: requests});
    });
});

router.post("/make_donation", auth(['donor', 'admin']), async (req, res) => {
    const {event_name, donor_email, recipient_email, items}=req.body;

    /* istanbul ignore next */
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

router.post("/update_pledge", auth(['donor', 'admin']), async (req, res) => {
    const {id, item_quantities}=req.body;

    const alreadyExistsPledge=await Pledge.findOne({where: {id: id}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsPledge) {
        alreadyExistsPledge.update({
            item_quantities: item_quantities
        }).then(function() { 
            return res.json({message: "Pledge Successfull!"});
        })
    }
});

router.get("/get_pledges", auth(['donor', 'admin']), async (req, res) => {
    Pledge.findAll({}, {raw: true}).then(pledges => {
        console.log(pledges)
        res.json({pledges: pledges});
    });
});

router.post("/pledge_resources", auth(['donor']), async (req, res) => {
    const {email, item_quantities}=req.body;
    
    const newPledge=new Pledge({email, item_quantities});
    /* istanbul ignore next */
    const savedPledge=await newPledge.save().catch((err)=> {
        console.log("Error: ", err);
        res.json({error: "Cannot save pledge at the moment!"}); });

    if (savedPledge) res.json({message: "Pledge made successfully"});
});
module.exports = router;