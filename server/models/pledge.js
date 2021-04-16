const { DataTypes } = require("sequelize");
const sequelize = require("../database");

const Pledge = sequelize.define("Pledge", {
  email: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  item_quantities: {
    type: DataTypes.STRING
  }
});

module.exports = Pledge;
