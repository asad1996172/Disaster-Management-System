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

    const adminUser=new User({
        fullName: 'Admin',
        email: 'admin@admin.com',
        password: '123456',
        role: 'admin',
        zipcode: 'zipcode'
    });

    const recipientUser=new User({
        fullName: 'Recipient',
        email: 'recipient@recipient.com',
        password: '123456',
        role: 'recipient',
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

    it("Make Donation", async () => {
        
        await adminUser.save().catch((err)=> {
            console.log("Error: ", err);
        });
        
        const admin = {
            email: 'admin@admin.com',
            password: '123456',
        };
        
        let jwtToken = '';

        await request(app)
        .post("/api/v1/login")
        .send(admin)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome Back!');
            jwtToken = response.body.token;
        });

        const event = {
            event_name:'Katrina',
            disaster_type: 'Hurricane',
            severity: 'extreme',
            location: 'Louisiana',
            event_date: '2006-05-01',
            zipcode: '70601',
            items: ''
        };

        await request(app)
        .post("/api/v1/create_event")
        .set({'x-auth-token': jwtToken})
        .send(event)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Event Created!');
        });
        
        await donorUser.save().catch((err)=> {
            console.log("Error: ", err);
        });
        
        const donor = {
            email: 'donor@donor.com',
            password: '123456',
        };
        
        jwtToken = '';

        await request(app)
        .post("/api/v1/login")
        .send(donor)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome Back!');
            jwtToken = response.body.token;
        });

        await recipientUser.save().catch((err)=> {
            console.log("Error: ", err);
        });
        
        const recipient = {
            email: 'recipient@recipient.com',
            password: '123456',
        };
        
        jwtToken = '';

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
            'email': 'recipient@recipient.com',
            'item_quantities': 'Blankets:20'
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
        
        const admin_2 = {
            email: 'admin@admin.com',
            password: '123456',
        };
        
        jwtToken = '';

        await request(app)
        .post("/api/v1/login")
        .send(admin_2)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome Back!');
            jwtToken = response.body.token;
        });
        
        await request(app)
        .post("/api/v1/make_donation")
        .set({'x-auth-token': jwtToken})
        .send({'event_name': 'Katrina', 'donor_email': 'donor@donor.com', 'recipient_email': 'recipient@recipient.com', 'items': ''})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Donation Successfull!');
        });

        await request(app)
        .post("/api/v1/delete_event")
        .set({'x-auth-token': jwtToken})
        .send({'event_name': event['event_name']})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Event deleted successfully');
        });

        await request(app)
        .post("/api/v1/delete_event")
        .set({'x-auth-token': jwtToken})
        .send({'event_name': event['event_name']})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Event doesnot exist');
        });
        
    });

    it("Get Pledges", async () => {
        
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
        .get("/api/v1/get_pledges")
        .set({'x-auth-token': jwtToken})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
        });
        
    });

    it("Pledge Resources", async () => {
        
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
        .post("/api/v1/pledge_resources")
        .set({'x-auth-token': jwtToken})
        .send({'email': 'donor@donor.com', 'item_quantities': 'Blankets:20'})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Pledge made successfully');
        });
        
    });

    // After all tersts have finished, close the DB connection
    afterAll(async () => {
        await sequelize.close()
    })
});