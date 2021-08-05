import { is_valid_change_password } from "./validations.js"

document.addEventListener("DOMContentLoaded",(e) => {
    const current_password_input = document.getElementById("current_password");
    const new_password_input = document.getElementById("new_password");
    const confirmation_input = document.getElementById("confirmation");
    const change_button = document.getElementById("change_button");

    const current_password_error_container = document.getElementById("current_password_error");
    const new_password_error_container = document.getElementById("new_password_error");
    const confirmation_error_container = document.getElementById("confirmation_error");

    change_button.addEventListener("click", (e) => {
        const current_password = current_password_input.value.trim();
        const new_password = new_password_input.value.trim();
        const confirmation = confirmation_input.value.trim();

        if (!is_valid_change_password(
            current_password, current_password_error_container,
            new_password, new_password_error_container,
            confirmation, confirmation_error_container
        )) {
            e.preventDefault();
        }
    });
});