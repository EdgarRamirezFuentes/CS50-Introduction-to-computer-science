// Form fields
const nameField = document.getElementById("nameInput");
const emailField = document.getElementById("mailInput");
const messageField = document.getElementById("messageInput");

console.log()
// Submit button
const submitBtn = document.getElementById("submitBtn");

// Error message labels
const nameError = document.getElementById("nameError");
const emailError = document.getElementById("emailError");
const messageError = document.getElementById("messageError");

// Functions
function isEmpty(text, messageLabel) {
    if (!text.length) {
        messageLabel.innerHTML = "This field is required";
        return true;
    }
    messageLabel.innerHTML = "";
    return false;
}

function isValidName(nameValue, messageLabel) {
    const nameRegex = /^[a-záéíóú\s]+$/gi;
    if (isEmpty(nameValue, messageLabel)) {
        return false;
    } else if (nameValue.length > 100) {
        messageLabel.innerHTML = "This field only accepts 100 characters.  Current characters:";
        return false;
    } else if (!nameRegex.test(nameValue)) {
        messageLabel.innerHTML = "This field only accepts letters";
        return false;
    }
    return true;
}

function isValidEmail(email, messageLabel) {
    // Regex flags 
    // g -> global search
    // i -> in-sensitive case
    const mailRegex = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/gi;
    if (isEmpty(email, messageLabel)) {
        return false;
    } else if (!mailRegex.test(email)) {
        messageLabel.innerHTML = "Enter a valid email";
        return false;
    }
    messageLabel.innerHTML = "";
    return true;
}

function isValidMessage(message, messageLabel) {
    // Regex flags 
    // g -> global search
    // i -> in-sensitive case
    if (message.length > 100) {
        messageLabel.innerHTML = "This field only accepts 100 characters.  Current characters:";
        return false;
    } else if (isEmpty(message, messageError)) {
        return false;
    }
    return true;
}

function clearForm() {
    messageField.value = "";
    nameField.value = "";
    emailField.value = "";
    nameError.innerHTML = "";
    emailError.innerHTML = "";
    messageError.innerHTML = "";
}

function isValidForm() {
    const nameValue = nameField.value.trim();
    const emailValue = emailField.value.trim();
    const messageValue = messageField.value.trim();
    const emailStatus = isValidEmail(emailValue, emailError);
    const messageStatus = isValidMessage(messageValue, messageError);
    const nameStatus = isValidName(nameValue, nameError);
    return emailStatus && nameStatus  && messageStatus ;
}

// Event listeners

nameField.addEventListener("", () => {

});

emailField.addEventListener("", () => {

});

messageField.addEventListener("change", () => {
    let length = messageField.value.trim().length;
    if (length > 100) {
        messageError.innerHTML = "This field only accepts 100 characters\nCurrent characters: " + length;
    }else {
        messageError.innerHTML= "";
    }
});

submitBtn.addEventListener("click", () => {
    Swal.fire({
        title: 'Are you sure that you want to send this message?',
        icon: 'question',
        showCancelButton: 1,
        confirmButtonText: 'Yes, send message',
        cancelButtonText: 'No, cancel',
        cancelButtonColor: '#ff4d4d',
    }).then((answer)=> {
        if(answer.isConfirmed) {
            if (isValidForm()) {
                Swal.fire('The message was sent', '', 'success');
                clearForm();
            } else {
                Swal.fire('The data is not correct', '', 'error');
            }
        }
    });
})