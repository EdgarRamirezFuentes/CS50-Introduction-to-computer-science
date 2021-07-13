document.addEventListener('DOMContentLoaded', (e) => {
    const nameInput = document.getElementById("name");
    const monthInput = document.getElementById("month");
    const dayInput = document.getElementById("day");
    const submitButton = document.getElementById("submit-btn");
    let errors = [];

    submitButton.addEventListener("click", (e) => {
        if (!isValidData()) {
            e.preventDefault();
            Swal.fire({
              title: 'Error!',
              text: "The data is not correct",
              icon: 'error',
              confirmButtonText: 'Cool'
            });
        }
    });

    function isValidData() {
        const month = monthInput.value.trim();
        const day = dayInput.value.trim();
        const name = nameInput.value.trim();
        const validName = isValidName(name);
        const validMonth = isValidMonth(month);
        const validDay = isValidDay(day);
        return validDay && validMonth && validName;
    }

    function isValidMonth(month) {
        const monthRegex = /^[1-9]{1,2}$/
        if (isEmpty(month) || !monthRegex.test(month) || parseInt(month) < 1 || parseInt(month) > 12) {
            return false;
        }
        return true;
    }

    function isValidDay(day) {
        const dayRegex = /^[1-9]{1,2}$/
        if (isEmpty(day) || !dayRegex.test(day) || parseInt(day) < 1 || parseInt(day) > 31) {
            errors.push("The day field is required");
            return false;
        }
        return true;
    }

    function isValidName(name) {
        const nameRegex = /^[a-záéíóú\s]+$/gi;
        if (isEmpty(name) || !nameRegex.test(nameValue)  || nameValue.length > 100) {
            return false;
        }
        return true;
    }

    function isEmpty(value) {
        return !value.length ? true : false;
    }

});