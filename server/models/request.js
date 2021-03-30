const { DataTypes } = require("sequelize");
const sequelize = require("../database");

const Request = sequelize.define("Request", {
  event_name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  item_quantities: {
    type: DataTypes.STRING
  }
});

module.exports = Request;
