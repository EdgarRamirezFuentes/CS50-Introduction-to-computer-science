import {
    is_empty
} from "./validation.js"
document.addEventListener("DOMContentLoaded", (e) => {
    /// input:text where the user input its new username
    const username = document.getElementById("username");
    /// input:text where the user input its new password
    const password = document.getElementById("password");
    /// button:submit where the user clicks to send its credentials
    const login_button = document.getElementById("login-button");

    /// p tag used to show any error message refered to the username
    const username_error = document.getElementById("username_error");
    /// p tag used to show any error message refered to the password
    const password_error = document.getElementById("password_error");

    login_button.addEventListener("click", (e) => {
        if (!is_valid_data()) {
            e.preventDefault();
        }
    });

    /**
     * Evaluate that each field requirements in the form are fulfilled and is true if that happens
     * @return {bool}
     */
    function is_valid_data() {
        /// Get the cleaned value in the username field
        const username_value = username.value.trim();
        /// Get the cleaned value in the password field
        const password_value = password.value.trim();

        const valid_username = !is_empty(username_value);
        const valid_password = !is_empty(password_value);

        if (!valid_username) username_error.innerHTML = "This field is required";
        if (!valid_password) password_error.innerHTML = "This field is required";

        return valid_username && valid_password ? true : false;
    }
});