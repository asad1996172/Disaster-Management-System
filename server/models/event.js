const { DataTypes } = require("sequelize");
const sequelize = require("../database");

const Event = sequelize.define("Event", {
  event_name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  disaster_type: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  severity: {
    type: DataTypes.ENUM('mild', 'medium', 'extreme')
  },
  location: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  event_date: {
    type: DataTypes.DATE,
    allowNull: false,
  },
  zipcode: {
    type: DataTypes.STRING,
    allowNull: true,
  },
  items: {
    type: DataTypes.STRING
  }
});

module.exports = Event;
