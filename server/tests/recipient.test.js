const request = require('supertest');
const app = require('../server');
const sequelize = require("../database");
const User = require("../models/user");
const Event = require("../models/event");

describe("Test Recipient Dashboard", async () => {
    // Set the db object to a variable which can be accessed throughout the whole test file
    beforeAll(async () => {
        await sequelize.sync({ force: true })
    })

    const recipientUser=new User({
        fullName: 'Recipient',
        email: 'recipient@recipient.com',
        password: '123456',
        role: 'recipient',
        zipcode: '52242'
    });

    it("Accessing Recipient Dashboard and Making Resource Request", async () => {
        
        await recipientUser.save().catch((err)=> {
            console.log("Error: ", err);
        });
        
        const recipient = {
            email: 'recipient@recipient.com',
            password: '123456',
        };
        
        let jwtToken = '';

        await request(app)
        .post("/api/v1/login")
        .send(recipient)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome Back!');
            jwtToken = response.body.token;
        });

        await request(app)
        .get("/api/v1/recipient")
        .set({'x-auth-token': jwtToken})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome to Recipient Page!');
        });

        resource_request_payload = {
            'event_name': 'Katrina',
            'email': 'asad@gmail.com',
            'item_quantities': ''
        }

        await request(app)
        .post("/api/v1/request_resources")
        .set({'x-auth-token': jwtToken})
        .send(resource_request_payload)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Request Created!');
        });

        await request(app)
        .post("/api/v1/request_resources")
        .set({'x-auth-token': jwtToken})
        .send(resource_request_payload)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Request already exists!');
        });
        
    });

    // After all tersts have finished, close the DB connection
    afterAll(async () => {
        await sequelize.close()
    })
});