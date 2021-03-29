const request = require('supertest');
const app = require('../server');
const sequelize = require("../database");
const User = require("../models/user");
const Event = require("../models/event");

describe("Test Donor Dashboard", async () => {
    // Set the db object to a variable which can be accessed throughout the whole test file
    beforeAll(async () => {
        await sequelize.sync({ force: true })
    })

    const donorUser=new User({
        fullName: 'Donor',
        email: 'donor@donor.com',
        password: '123456',
        role: 'donor',
        zipcode: '52242'
    });

    it("Accessing Donor Dashboard", async () => {
        
        await donorUser.save().catch((err)=> {
            console.log("Error: ", err);
        });
        
        const donor = {
            email: 'donor@donor.com',
            password: '123456',
        };
        
        let jwtToken = '';

        await request(app)
        .post("/api/v1/login")
        .send(donor)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome Back!');
            jwtToken = response.body.token;
        });

        await request(app)
        .get("/api/v1/donor")
        .set({'x-auth-token': jwtToken})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome to Donor Page!');
        });
        
    });

    it("Accessing Donor Dashboard without JWT", async () => {

        await request(app)
        .get("/api/v1/donor")
        .set({'x-auth-token': ''})
        .then(async (response) => {
            expect(response.statusCode).toBe(401);
            expect(response.body.message).toBe('No token, authorization denied');
        });
        
    });

    it("Accessing Donor Dashboard with wrong JWT", async () => {

        await request(app)
        .get("/api/v1/donor")
        .set({'x-auth-token': 'something random'})
        .then(async (response) => {
            expect(response.statusCode).toBe(401);
            expect(response.body.message).toBe('Token is not valid');
        });
        
    });

    it("Accessing Recipient Dashboard with Donor User", async () => {
        
        await donorUser.save().catch((err)=> {
            console.log("Error: ", err);
        });
        
        const donor = {
            email: 'donor@donor.com',
            password: '123456',
        };
        
        let jwtToken = '';

        await request(app)
        .post("/api/v1/login")
        .send(donor)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome Back!');
            jwtToken = response.body.token;
        });

        await request(app)
        .get("/api/v1/recipient")
        .set({'x-auth-token': jwtToken})
        .then(async (response) => {
            expect(response.statusCode).toBe(401);
            expect(response.body.message).toBe('Restricted Access');
        });
        
    });

    // After all tersts have finished, close the DB connection
    afterAll(async () => {
        await sequelize.close()
    })
});