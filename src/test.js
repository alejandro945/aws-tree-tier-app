const expect = require('chai').expect;
const connection = require('./app');

describe('MySQL Connection', () => {
  it('should connect to the MySQL database', () => {
    expect(connection.state).to.equal('connected');
  });
});
