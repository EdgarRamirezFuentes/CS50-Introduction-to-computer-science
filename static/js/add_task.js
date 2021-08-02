import {is_valid_task_data} from "./validations.js"

document.addEventListener("DOMContentLoaded", (e) => {
    const title_input = document.getElementById("title");
    const description_input = document.getElementById("description");
    const add_task_button = document.getElementById("add_task_button");

    const title_error_container = document.getElementById("title_error");
    const description_error_container = document.getElementById("description_error");
    const description_length_container = document.getElementById("description_length");
    const title_length_container = document.getElementById("title_length");

    add_task_button.addEventListener("click", (e) => {
        const title = title_input.value.trim();
        const description = description_input.value.trim();
        if (!is_valid_task_data(
            title, title_error_container, 
            description, description_error_container)) {
            e.preventDefault();
        }
    });

    title_input.addEventListener("keyup", (e) => {
        const title_length = title_input.value.trim().length;
        if (title_length > 50) {
            e.preventDefault();
            title_error_container.innerHTML = "The max length of this field is 50 characters";
        } else {
            title_error_container.innerHTML = "";
        }
        title_length_container.innerHTML = title_length;
    });

    description_input.addEventListener("keyup", (e) => {
        const description_length = description_input.value.trim().length;
        if (description_length > 100) {
            e.preventDefault();
            description_error_container.innerHTML = "The max length of this field is 100 characters";
        } else {
            description_error_container.innerHTML = "";
        }
        description_length_container.innerHTML = description_length;
    });
});