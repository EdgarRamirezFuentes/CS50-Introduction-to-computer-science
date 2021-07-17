
    /**
    * Evaluates wether the value is empty or not. If the value is empty, returns true
    * @param {string} value is the value that will be evaluated
    * @return {bool} true if is empty, else false
    */
    function is_empty(value) {
        return !value.length ? true : false;
    }

    /**
     * Evaluates that the username is valid by checking that it is not an empty string and
     * checking that matches the established pattern. If any of these requirements is not fulfilled
     * a message will be shown in the message container and will return false;
     * @param {string} username_value is the value that will be evaluated
     * @param {HTMLElement} <p> tag used to show the error message if there is an error
     * @return {bool}
     */
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
            return false;
        } else if (!username_regex.test(username_value)) {
            message_container.innerHTML = "Enter a valid username";
            return false;
        } else {
            message_container.innerHTML = "";
        }

        return true;
    }

    /**
     * Evaluates that the password is valid by checking that it is not an empty string and
     * checking that matches the established pattern. If any of these requirements is not fulfilled
     * a message will be shown in the message container and will return false;
     * @param {string} password_value is the value that will be evaluated
     * @param {HTMLElement} <p> tag used to show the error message if there is an error
     * @return {bool}
     */
    function is_valid_password(password_value, message_container) {
        /*
            Password requirements:
                - Password consists of alphanumeric characters (a-z0-9), lowercase, or uppercase.
                - The number of characters must be between 8 to 10.
        */
        const password_regex = /^[a-z0-9]{8,10}$/gi;
        if (is_empty(password_value))  {
            message_container.innerHTML = "This field is required";
            return false;
        } else if (!password_regex.test(password_value)) {
            message_container.innerHTML = "Enter a valid password";
            return false;
        } else {
            message_container.innerHTML = "";
        }
        return true;
    }

    /**
     * Evaluates that the password and its confirmation password match. If these two do not match,
     * a message will be shown in the message container and will return false;
     * @param {string} password_value is the value that will be compared
     * * @param {string} confirmaton_value is the value that will be compared
     * @param {HTMLElement} <p> tag used to show the error message if there is an error
     * @return {bool}
     */
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

    function is_valid_share(share_value) {
        const share_regex = /^[0-9]{1,3}$/
        return share_regex.test(share_value);
    }

    export {is_empty, is_valid_username, is_valid_password, is_confirmed_password, is_valid_share};