
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
    const valid_username = is_valid_username(username);
    const valid_password = is_valid_password(password);
    const valid_email = email.length ? is_valid_email(email) : true;
    const valid_confirmation = password == confirmation ? true : false;

    // Username messages
    if (!username.length) {
        username_error_container.innerHTML = "This field is required";
    } else if (!valid_username) {
        username_error_container.innerHTML = "Input a valid username";
    } else {
        username_error_container.innerHTML = "";
    }

    // Password messages
    if (!password.length) {
        password_error_container.innerHTML = "This field is required";
    } else if (!valid_password) {
        password_error_container.innerHTML = "Input a valid password";
    } else {
        password_error_container.innerHTML = "";
    }

    // Note: The email is not required at all
    if (email.length && !valid_email) { 
        email_error_container = "Input a valid email";
    } else {
        email_error_container.innerHTML = "";
    }

    // Confirmation messages
    if (!confirmation.length) {
        confirmation_error_container.innerHTML = "This field is required";
    } else if (!valid_confirmation) {
        confirmation_error_container.innerHTML = "The confirmation does not match the password";
    } else {
        confirmation_error_container.innerHTML = "";
    }

    return valid_username && valid_password && valid_email && valid_password;
}

/**
 * Check if the provided username is valid
 * @param {string} username is the username that the user input
 * @return {boolean} true if the username is valid, otherwise return false
 */
function is_valid_username(username) {
    // Username requirements
    // - Only accept alphanumeric characters
    // - The first letter must be a letter
    // - The length of the username must be between 6 to 16 characters
    const username_re = /^[a-z][a-z0-9]{5,15}$/gi
    return username_re.test(username);
}

/**
 * Check if the provided email is valid
 * @param {string} email is the email that the user input
 * @return {bool} true iif the email is valid, otherwise return false
 */ 
function is_valid_email(email) {
    // Regex source: https://www.abstractapi.com/tools/email-regex-guide
    const email_re = /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    return  email_re.test(email);
}

/**
 * Check if the provided password is valid
 * @param {string} password is the password that the user input
 * @return {boolean} true if the password is valid, otherwise false
 */
function is_valid_password(password) {  
    // Password requirements
    // - Only accepts alphanumeric characters
    // - The length of the username must be between 8 to 20 characters
    const password_re =/^[a-z0-9]{8,20}$/gi;
    return password_re.test(password);
}

/**
 * Check if all the field in the registration form are valid
 * @param {string} title is the title that the user input
 * @param {HTMLElement} title_error_container is the container where the
 *                      error messages regarding to the title input will be
 *                      displayed.
 * @param {string} description is the description that the user input
 * @param {HTMLElement} description_error_container is the container where the
 *                      error messages regarding to the description input will be
 *                      displayed.
 * @return {boolean} true if the data is valid, otherwise return false
 */ 

function is_valid_task_data(
    title, title_error_container,
    description, description_error_container
) {
    let valid_data = true;
    if (!title.length) {
        title_error_container.innerHTML = "This field is required";
        valid_data = false;
    } else {
        title_error_container.innerHTML = "";
    }

    if (title.length > 50) {
        title_error_container.innerHTML = "The max length of this field is 50 characters";
        valid_data = false;
    } else {
        title_error_container.innerHTML = "";
    } 

    if (description.length > 100) {
        description_error_container.innerHTML = "The max length of this field is 100 characters";
        valid_data = false;
    } else {
        description_error_container.innerHTML = "";
    }
    return valid_data;
}

function is_valid_change_password(
    current_password, current_password_error_container,
    new_password, new_password_error_container,
    confirmation, confirmation_error_container
) {
    let valid_data = true;
    if (!current_password.length) {
        current_password_error_container.innerHTML = "This field is required";
        valid_data = false;
    } else {
        current_password_error_container.innerHTML = "";
    }

    if (!new_password.length) {
        new_password_error_container.innerHTML = "This field is required";
        valid_data = false;
    } else if (!is_valid_password(new_password)) {
        new_password_error_container.innerHTML = "Input a valid new password";
        valid_data = false;
    } else {
        new_password_error_container.innerHTML = "";
    }

    if (!confirmation.length) {
        confirmation_error_container.innerHTML = "This field is required";
        valid_data = false;
    } else if (new_password != confirmation) {
        confirmation_error_container.innerHTML = "The confirmation does not match the new password";
        valid_data = false;
    } else {
        confirmation_error_container.innerHTML = "";
    }
    return valid_data;
}
export {
    is_valid_registration_data, 
    is_valid_task_data,
    is_valid_change_password
};