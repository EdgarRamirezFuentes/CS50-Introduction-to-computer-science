import {
    is_empty,
    is_valid_username,
    is_valid_password,
    is_confirmed_password
} from "./validation.js";
document.addEventListener("DOMContentLoaded", (e) => {
    /// input:text where the user input its new username
    const username = document.getElementById("username");
    /// input:text where the user input its new password
    const password = document.getElementById("password");
    /// input:text where the user input the confirmation of its new password
    const confirmation = document.getElementById("confirmation");
    /// button:submit where the user clicks to send its information
    const register_button = document.getElementById("register-button");

    /// p tag used to show any error message refered to the username
    const username_error = document.getElementById("username_error");
    /// p tag used to show any error message refered to the password
    const password_error = document.getElementById("password_error");
    /// p tag used to show any error message refered to the confirmation password
    const confirmation_error = document.getElementById("confirmation_error");


    register_button.addEventListener("click", (e) => {
        /// If something went wrong, the submit event is stopped
        if (!is_valid_data()) {
            e.preventDefault();
        }
    });

    /**
     * Evaluate that each field requirements in the form are fulfilled and is true id that happens
     * @return {bool}
     */
    function is_valid_data() {
        /// Get the cleaned value in the username field
        const username_value = username.value.trim();
        /// Get the cleaned value in the password field
        const password_value = password.value.trim();
        /// Get the cleaned value in the confirmation password field
        const confirmation_value = confirmation.value.trim();

        const valid_username = is_valid_username(username_value, username_error);
        const valid_password = is_valid_password(password_value, password_error);
        const confirmed_password = is_confirmed_password(password_value, confirmation_value, confirmation_error);

        return valid_username && valid_password && confirmed_password ? true : false;
    }
});