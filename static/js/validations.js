
/**
 * Check if all the field in the registration form are valid
 * @param {string} username is the username that the user input
 * @param {HTMLElement} username_error_container is the container where the
 *                      error messages regarding to the username input will be
 *                      displayed.
 * @param {string} email is the email that the user input
 * @param {HTMLElement} email_error_container is the container where the
 *                      error messages regarding to the email input will be
 *                      displayed.
 * @param {string} password is the password that the user input
 * @param {HTMLElement} password_error_container is the container where the
 *                      error messages regarding to the password input will be
 *                      displayed.
 * @param {string} confirmation is the confirmation password that the user input
 * @param {HTMLElement} confirmation_error_container is the container where the
 *                      error messages regarding to the confirmation password input will be
 *                      displayed.
 * @return {boolean} true if the data is valid, else false.
 */ 

function is_valid_registration_data(
    username, username_error_container, 
    email, email_error_container,
    password, password_error_container, 
    confirmation, confirmation_error_container
) {

}

function is_valid_username(username) {

}

function is_valid_email(email) {

}

function is_valid_password(password, confirmation) {

}

export {
    is_valid_registration_data, 
};