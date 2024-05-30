(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav: true,
        navText: [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 2
            },
            1200: {
                items: 2
            }
        }
    });


    // puja carousel
    $(".puja-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav: true,
        navText: [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });
})(jQuery);


// popup 
function openPopup() {
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    // Get the last three navigation links
    var templesLink = document.getElementById("templesLink");
    var testimonialLink = document.getElementById("testimonialLink");
    var contactLink = document.getElementById("contactLink");

    // Add click event listeners to the last three links
    templesLink.addEventListener('click', function (event) {
        event.preventDefault();
        openPopup();
    });

    testimonialLink.addEventListener('click', function (event) {
        event.preventDefault();
        openPopup();
    });

    contactLink.addEventListener('click', function (event) {
        event.preventDefault();
        openPopup();
    });
});



// admin details popup 
function openAdminLogin() {
    var modal = document.getElementById("adminLoginModal");
    modal.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById("adminLoginModal");
    modal.style.display = "none";
}

function validateAdminLogin() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Static credentials for demonstration
    var staticEmail = "a@gmail.com";
    var staticPassword = "admin";

    if (email === staticEmail && password === staticPassword) {
        // Redirect to admin.html if credentials are correct
        window.location.href = "/admin";
        return false; // Prevent form submission
    } else {
        // Display error message
        var errorMessage = document.getElementById("errorMessage");
        errorMessage.style.display = "block";

        // Hide error message after 2 seconds
        setTimeout(function () {
            errorMessage.style.display = "none";
        }, 2000);

        return false; // Prevent form submission
    }
}

// when product added then it redirects the page where it started 

// Function to set a cookie with expiration time
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// Function to get a cookie value
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}



// Function to handle adding an item to the cart
function addToCart(itemId) {
    // Example function, adjust as needed
    // Here you can perform any logic related to adding an item to the cart
    // For example, making an AJAX request to add the item to the cart in the backend
    // Once the item is successfully added to the cart, you can save the scroll position
    setCookie('scrollPosition', window.scrollY, 1);
}

// pandit adding popup 
$(document).ready(function () {
    // When location is selected
    $('#locationSelect').change(function () {
        var location = $(this).val();

        // Update the pandit list based on the selected location
        updatePanditList(location);

        // Show/hide address and contact input based on location selection
        if (location) {
            $('#addressGroup').show();
            $('#contactGroup').show();
        } else {
            $('#addressGroup').hide();
            $('#contactGroup').hide();
        }
    });

    function addToCart() {
        var date = $('#deliveryDate').val();
        var time = $('#deliveryTime').val();
        var pandit = $('#panditSelect').val();
        var location = $('#locationSelect').val();
        var locationAddress = $('#locationAddress').val();
        var contactDetails = $('#contactDetails').val();

        // Check if any field is empty
        if (!date || !time || !pandit || !location || !locationAddress || !contactDetails) {
            alert("Please fill in all the fields.");
            return;
        }

        // Validate date format and other validations...

        // Perform further actions or submit the form
        // For now, let's just show an alert with the selected data
        alert("Selected Date: " + date + "\nSelected Time: " + time + "\nPandit: " + pandit + "\nLocation: " + location + "\nLocation Address: " + locationAddress + "\nContact Details: " + contactDetails);
        $('#cartPopup').modal('hide');
    }
});


// chat bot 
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector("#send-btn");
const endChatBtn = document.querySelector(".end-chat-btn");

let userMessage = null;
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p>${message}</p>` : `<span class="material-symbols-outlined">💬</span><p>${message}</p>`;
    chatLi.innerHTML = chatContent;
    return chatLi;
}

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }, 600);

    setTimeout(() => {
        chatbox.appendChild(createChatLi("We will connect you to our members. Please wait.", "incoming"));
        chatbox.scrollTo(0, chatbox.scrollHeight);
        chatInput.style.display = "none";
        endChatBtn.style.display = "inline-block";
    }, 1200);
}

chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", () => {
    handleChat();
    if (chatInput.value.trim() === "") {
        endChatBtn.style.display = "none";
    }
});

closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

endChatBtn.addEventListener("click", () => {
    document.body.classList.remove("show-chatbot");
    chatInput.style.display = "block";
    endChatBtn.style.display = "none";
});

// cursor script

document.addEventListener("DOMContentLoaded", function () {
    var cursor = document.getElementById("cursor");

    document.addEventListener("mousemove", function (e) {
        var x = e.clientX;
        var y = e.clientY;

        // Set the position of the cursor element to the mouse position
        cursor.style.left = x + "px";
        cursor.style.top = y + "px";
    });

    document.addEventListener("mouseenter", function () {
        cursor.style.backgroundColor = "#FF0000"; // Change color on mouse enter
    });

    document.addEventListener("mouseleave", function () {
        cursor.style.backgroundColor = "transparent"; // Restore transparency on mouse leave
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const cursor = document.querySelector('.cursor');

    document.addEventListener("mousemove", function (e) {
        const mouseX = e.clientX;
        const mouseY = e.clientY;
        cursor.style.left = mouseX + 'px';
        cursor.style.top = mouseY + 'px';
    });

    const clickableElements = document.querySelectorAll('a, button, input[type="button"], input[type="submit"], .cursor-hover');

    clickableElements.forEach(function (element) {
        element.addEventListener('mouseover', function () {
            cursor.classList.add('hover');
        });

        element.addEventListener('mouseout', function () {
            cursor.classList.remove('hover');
        });
    });
});
