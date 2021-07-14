document.addEventListener("DOMContentLoaded", (e) => {
    // Inputs and buttons
   const username = document.getElementById("username");
   const password = document.getElementById("password");
   const confirmation = document.getElementById("confirmation");
   const register_button = document.getElementById("register-button");

    // Error messages
    const username_error = document.getElementById("username_error");
    const password_error = document.getElementById("password_error");
    const confirmation_error = document.getElementById("confirmation_error");

    // Event Listeners
    register_button.addEventListener("click", (e) => {
        if (!is_valid_data()) {
            e.preventDefault();
        }
    });

    // Functions

    function is_valid_data() {
        const username_value = username.value.trim();
        const password_value = password.value.trim();
        const confirmation_value = confirmation.value.trim();

        const valid_username = is_valid_username(username_value, username_error);
        const valid_password = is_valid_password(password_value, password_error);
        const confirmed_password = is_confirmed_password(password_value, confirmation_value, confirmation_error);

        return valid_username && valid_password && confirmed_password ? true : false;
    }

    function is_empty(value) {
        return !value.length ? true : false;
    }

    function is_valid_username(username_value, message_container) {
        /*
            Source: https://mkyong.com/regular-expressions/how-to-validate-username-with-regular-expression/
            Username requirements:
                - Username first character must be a letter [a-z]
                - Username consists of alphanumeric characters (a-z0-9), lowercase, or uppercase.
                - Username allowed of the dot (.), underscore (_), and hyphen (-).
                - The dot (.), underscore (_), or hyphen (-) must not be the first or last character.
                - The dot (.), underscore (_), or hyphen (-) does not appear consecutively, e.g., user..name
                - The number of characters must be between 5 to 20.
        */
        const username_regex = /^[a-z]([._-](?![._-])|[a-z0-9]){3,18}[a-z0-9]$/gi;
        if (is_empty(username_value))  {
            message_container.innerHTML = "This field is required";
            return;
        } else if (!username_regex.test(username_value)) {
            message_container.innerHTML = "Enter a valid username";
            return false;
        } else {
            message_container.innerHTML = "";
        }

        return true;
    }

    function is_valid_password(password_value, message_container) {
        /*
            Password requirements:
                - Password consists of alphanumeric characters (a-z0-9), lowercase, or uppercase.
                - Username allowed special characters.
                - The number of characters must be between 8 to 10.
        */
        const password_regex = /^[a-z0-9!"#\$%&'\(\)\*\+,-\.\/:;<=>\?@[\]\^_`\{\|}~]{8,10}$/gi;
        if (is_empty(password_value))  {
            message_container.innerHTML = "This field is required";
            return;
        } else if (!password_regex.test(password_value)) {
            message_container.innerHTML = "Enter a valid password";
            return false;
        } else {
            message_container.innerHTML = "";
        }
        return true;
    }

    function is_confirmed_password(password_value, confirmation_value, message_container) {
        if (is_empty(confirmation_value, message_container)) {
            message_container.innerHTML = "This field is required";
            return false;
        } else if (password_value != confirmation_value) {
            message_container.innerHTML = "The password does not match this field";
            return false;
        }
        message_container.innerHTML = "";
        return true;
    }
});