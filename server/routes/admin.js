const auth = require('../middleware/auth');
const express = require("express");

const router = express.Router();

router.get("/admin", auth(['admin']), async (req, res) => {
    res.json({ message: "Welcome to Admin Page!"});
});

module.exports = router;