const request = require('supertest');
const app = require('../server');
const sequelize = require("../database");
const User = require("../models/user");
const Event = require("../models/event");

describe("Test Admin Dashboard", async () => {
    // Set the db object to a variable which can be accessed throughout the whole test file
    beforeAll(async () => {
        await sequelize.sync({ force: true })
    })

    const adminUser=new User({
        fullName: 'Admin',
        email: 'admin@admin.com',
        password: '123456',
        role: 'admin',
        zipcode: 'zipcode'
    });

    it("Accessing Admin Dashboard", async () => {
        
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

        await request(app)
        .get("/api/v1/admin")
        .set({'x-auth-token': jwtToken})
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Welcome to Admin Page!');
        });
        
    });

    it("Creating Event", async () => {
        
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

    // After all tersts have finished, close the DB connection
    afterAll(async () => {
        await sequelize.close()
    })
});