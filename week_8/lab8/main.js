// html elements part 1
const bruce = document.getElementById("bruce");
const barry = document.getElementById("barry");
const hal = document.getElementById("hal");
const dick = document.getElementById("dick");
const answer1 = document.getElementById("answer1");
const buttons = document.querySelectorAll(".btn1");
console.log(barry, answer1);

// html elements part 2
const answer2 = document.getElementById("answer2");
const answer3 = document.getElementById("answer3");
const buttonCheck = document.getElementById("checkAnswer");

// answer messages

// Functions
function correctAnswer(option, messageContainer) {
    clearButtons();
    option.style.backgroundColor = '#00FF00';
    messageContainer.innerHTML = "Correct!";
}

function clearButtons() {
    buttons.forEach(button => {
        button.style.backgroundColor = "#D9EDFF";
    });
}

function wrongAnswer(option, messageContainer) {
    clearButtons();
    option.style.backgroundColor = '#FF0000';
    messageContainer.innerHTML = "Incorrect";
}

// Part 1:

barry.addEventListener("click", () =>  correctAnswer(barry, answer1));

bruce.addEventListener("click", () =>  wrongAnswer(bruce, answer1));

hal.addEventListener("click", () => wrongAnswer(hal, answer1));

dick.addEventListener("click", () => wrongAnswer(dick, answer1));

// Part 2

buttonCheck.addEventListener("click", () => {
    answer3.value.trim().toLowerCase() == "optimus prime" ? correctAnswer(answer3, answer2) : wrongAnswer(answer3, answer2);
    window.setTimeout(() => {
        answer3.style.backgroundColor = "#FFFFFF";
        answer2.innerHTML = "";
        answer3.value = "";
    }, 3000);
});