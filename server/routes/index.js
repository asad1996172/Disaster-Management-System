const express = require("express");
const registerApi = require("./register");
const loginApi = require("./login");
const adminApi = require("./admin");

const router = express.Router();

router.use(registerApi);
router.use(loginApi);
router.use(adminApi);

module.exports = router;
