const auth = require('../middleware/auth');
const express = require("express");

const router = express.Router();

router.get("/donor", auth(['donor']), async (req, res) => {
    res.json({ message: "Welcome to Donor Page!"});
});

module.exports = router;