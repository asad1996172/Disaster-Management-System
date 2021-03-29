const express = require("express")
const User = require("../models/user")

const router = express.Router()

// @route   POST /register
// @desc    Register user
// @access  Public
router.post("/register", async (req, res)=> {
    const {fullName, email, password, role, zipcode}=req.body;

    const alreadyExistsUser=await User.findOne({where: {email}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsUser) {
        return res.json({message: "User with email already exists!"});}

    const alreadyExistsAdmin=await User.findOne({where: {role}}).catch(
        (err)=> {
            console.log("Error: ", err);}
    );

    if (alreadyExistsAdmin) {
        return res.json({message: "An admin user already exists!"});}

    const newUser=new User({fullName, email, password, role, zipcode});
    const savedUser=await newUser.save().catch((err)=> {
        console.log("Error: ", err);
        res.json({error: "Cannot register user at the moment!"}); });

    if (savedUser) res.json({message: "Thanks for registering"}); 
})


// @route   POST /delete_user
// @desc    Delete user
// @access  Public
router.post("/delete_user", async (req, res)=> {
    const { email }=req.body;

    const alreadyExistsUser=await User.findOne({where: {email}});
    if (alreadyExistsUser) {
        await User.destroy({where: {email}})
        return res.json({message: "User deleted successfully"});
    }

    return res.json({message: "User doesnot exist"});
})

module.exports = router
