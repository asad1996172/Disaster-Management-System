const express = require("express");
const User = require("../models/user");
const jwt = require("jsonwebtoken");

const router = express.Router();

router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  const userWithEmail = await User.findOne({ where: { email } }).catch(
    (err) => {
      console.log("Error: ", err);
    }
  );
  console.log(email)
  if (!userWithEmail)
    return res.json({ message: "Email or password does not match!" });

  if (userWithEmail.password !== password)
    return res.json({ message: "Email or password does not match!" });
  
  const payload = {
      user: {
        id: userWithEmail.id,
        email: userWithEmail.email,
        role: userWithEmail.role
      },
    };
  const jwtToken = jwt.sign(
    payload,
    process.env.JWT_TOKEN
  );

  res.json({ message: "Welcome Back!", token: jwtToken });
});

module.exports = router;
