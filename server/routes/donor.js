const auth = require('../middleware/auth');
const Event = require("../models/event");
const Request = require("../models/request")
const express = require("express");

const router = express.Router();

router.get("/donor", auth(['donor']), async (req, res) => {
    Request.findAll({}, {raw: true}).then(requests => {
        console.log(requests)
        // requests will be an array of all Request instances
        Event.findAll({}, {raw: true}).then(events => {
            // requests will be an array of all Request instances
            console.log(events)
            res.json({ message: "Welcome to Donor Page!", requests: requests, events: events});
        });
    });
});

module.exports = router;