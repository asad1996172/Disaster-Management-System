const request = require('supertest')
const app = require('../server')
const sequelize = require("../database");
const User = require("../models/user")

describe("Test Authentication", () => {
    // Set the db object to a variable which can be accessed throughout the whole test file
    beforeAll(async () => {
        await sequelize.sync({ force: true })
    })

    it("Register Admin", async () => {
        const admin = {
            fullName:'John Doe',
            email: 'admin@admin.com',
            password: '123456',
            role: 'admin',
            zipcode: '52242'
        };
        await request(app)
        .post("/api/v1/register")
        .send(admin)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('Thanks for registering');
        });
    });

    it("Register Multiple Admin", async () => {
        const adminUser=new User({
            fullName: 'Admin',
            email: 'admin@admin.com',
            password: '123456',
            role: 'admin',
            zipcode: 'zipcode'
        });
        await adminUser.save().catch((err)=> {
            console.log("Error: ", err);
            res.json({error: "Cannot register user at the moment!"}); 
        });
        const admin = {
            fullName:'John Doe',
            email: 'admin_2@admin.com',
            password: '123456',
            role: 'admin',
            zipcode: '52242'
        };
        await request(app)
        .post("/api/v1/register")
        .send(admin)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('An admin user already exists!');
        });
    });

    it("Register Existing User", async () => {
        const adminUser=new User({
            fullName: 'Admin',
            email: 'admin@admin.com',
            password: '123456',
            role: 'admin',
            zipcode: 'zipcode'
        });
        await adminUser.save().catch((err)=> {
            console.log("Error: ", err);
            res.json({error: "Cannot register user at the moment!"}); 
        });
        const admin = {
            fullName:'John Doe',
            email: 'admin@admin.com',
            password: '123456',
            role: 'admin',
            zipcode: '52242'
        };
        await request(app)
        .post("/api/v1/register")
        .send(admin)
        .then(async (response) => {
            expect(response.statusCode).toBe(200);
            expect(response.body.message).toBe('User with email already exists!');
        });
    });

    // After all tersts have finished, close the DB connection
    afterAll(async () => {
        await sequelize.close()
    })
});