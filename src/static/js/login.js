document.addEventListener("DOMContentLoaded", function () {
    // Get the message elements
    var messages = document.querySelectorAll(".message");

    // Loop through each message element
    messages.forEach(function (message) {
        // Close the message after 2 seconds
        setTimeout(function () {
            message.style.display = "none";
        }, 3000);
    });
});

const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});