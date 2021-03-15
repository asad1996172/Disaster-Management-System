const express = require("express");
const registerApi = require("./register");
const loginApi = require("./login");
const adminApi = require("./admin");
const donorApi = require("./donor");
const recipientApi = require("./recipient");

const router = express.Router();

router.use(registerApi);
router.use(loginApi);
router.use(adminApi);
router.use(donorApi);
router.use(recipientApi);

module.exports = router;
