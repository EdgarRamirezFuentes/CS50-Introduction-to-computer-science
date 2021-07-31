import {is_valid_registration_data} from "./validations.js"

document.addEventListener("DOMContentLoaded", (e) => {
    const username_input = document.getElementById("username");
    const email_input = document.getElementById("email");
    const password_input = document.getElementById("password");
    const confirmation_input = document.getElementById("confirmation");
    const register_button = document.getElementById("register_button");

    const username_error_container = document.getElementById("username_error");
    const email_error_container = document.getElementById("email_error");
    const password_error_container = document.getElementById("password_error");
    const confirmation_error_container = document.getElementById("confirmation_error");

    register_button.addEventListener("click", (e) => {
        const username = username_input.value.trim();
        const email = email_input.value.trim();
        const password = password_input.value.trim();
        const confirmation = confirmation_input.value.trim();
        
        if(!is_valid_registration_data(
                username, username_error_container, 
                email, email_error_container,
                password, password_error_container, 
                confirmation, confirmation_error_container
        )) {
            e.preventDefault();
        }
    }); 
});