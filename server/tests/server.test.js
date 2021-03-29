const request = require('supertest')
const app = require('../server')


describe("Test homepage", () => {
  test("Gets the homepage route", done => {
    request(app)
      .get("/")
      .then(response => {
        expect(response.statusCode).toBe(200);
        expect(response.body.status).toBe('API Running');
        done();
      });
  });
});