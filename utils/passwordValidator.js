// passwordValidator.ts
const passwordValidator = require("password-validator");

// Create a schema
const schema = new passwordValidator();

// Add properties to it
schema
  .is()
; // Blacklist these values

// Validate a password and get detailed errors
const  validatePassword = (password) => {
  const errorMessages= [];

  if (!schema.validate(password)) {
    const validationErrors = schema.validate(password, {
      list: true,
    });
    errorMessages.push(...validationErrors.map((error) => error.message));
  }

  return errorMessages;
}
module.exports = validatePassword;