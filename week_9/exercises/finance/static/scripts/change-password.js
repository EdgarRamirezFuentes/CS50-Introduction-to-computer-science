import {
    is_empty,
    is_valid_password,
    is_confirmed_password
} from "./validation.js";

document.addEventListener("DOMContentLoaded", () => {
    const current_password = document.getElementById("current-password");
    const new_password = document.getElementById("new-password");
    const confirmation_password = document.getElementById("confirmation");
    const change_button = document.getElementById("change-button");


    const current_password_error = document.getElementById("password-error");
    const new_password_error = document.getElementById("new-password-error");
    const confirmation_error = document.getElementById("confirmation-error");

    change_button.addEventListener("click", (e) => {
        if (!is_valid_data()) {
            e.preventDefault();
        }
    });

    /**
     * Checks if the provided new password matches the pattern and if it is confirmed. If the password is correct return true
     * @return {bool}
     */
    function is_valid_data() {
        const current_password_value = current_password.value.trim()
        const new_password_value = new_password.value.trim();
        const confirmation_password_value = confirmation_password.value.trim();
        const valid_current_password = !is_empty(current_password_value);
        const valid_new_password = is_valid_password(new_password_value, new_password_error);
        const confirmed_password = is_confirmed_password(new_password_value, confirmation_password_value, confirmation_error)

        if (!valid_current_password) {
            current_password_error.innerHTML = "This field is required";
        } else {
            current_password_error.innerHTML = "";
        }

        return valid_current_password && valid_new_password && confirmed_password;
    }

});