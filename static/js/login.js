document.addEventListener("DOMContentLoaded" , (e) => {
    const username_input = document.getElementById("username");
    const password_input = document.getElementById("password");
    const login_button = document.getElementById("login_button");
    const remember_box = document.getElementById("remember");

    const username_error_container = document.getElementById("username_error");
    const password_error_container = document.getElementById("password_error");

    const remember_username = localStorage.getItem("username");
    if (remember_username) {
        username_input.value = remember_username;
        remember_box.checked = true;
    }

    login_button.addEventListener("click", (e) => {
        const username = username_input.value
        const password = password_input.value

        // Username messages
        if (!username.length) {
            username_error_container.innerHTML = "This field is required";
        } else {
            username_error_container.innerHTML = "";
        }

        // Password messages
        if (!password.length) {
            password_error_container.innerHTML = "This field is required";
        } else {
            password_error_container.innerHTML = "";
        }
        
        if (!username.length || !password.length) { 
            e.preventDefault(); 
        } else if  (remember_box.checked) {
            localStorage.setItem("username", username);
        } else if (!remember_box.checked) {
            localStorage.removeItem("username");
        }

    });
});