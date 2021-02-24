const sayHello = require('../dummy');

test('returns a personalized greeting', () => {
  expect(sayHello('Asad')).toBe("Hi, Asad.");
});