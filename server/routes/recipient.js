const auth = require('../middleware/auth');
const express = require("express");

const router = express.Router();

router.get("/recipient", auth(['recipient']), async (req, res) => {
    res.json({ message: "Welcome to Recipient Page!"});
});

module.exports = router;