const auth = require('../middleware/auth');
const Request = require("../models/request")
const express = require("express");

const router = express.Router();

router.get("/donor", auth(['donor']), async (req, res) => {
    Request.findAll({}, {raw: true}).then(requests => {
        // requests will be an array of all Request instances
        console.log(requests)
        res.json({ message: "Welcome to Donor Page!", requests: requests});
    });
});

module.exports = router;