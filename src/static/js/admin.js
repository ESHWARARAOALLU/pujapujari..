// function displayForm() {
//     var addItemForm = document.getElementById("addItemForm");
//     addItemForm.style.display = "block";
// }

// function addItem() {
//     var itemName = document.querySelector("input[name='name']").value;
//     var itemPrice = document.querySelector("input[name='price']").value;
//     var itemDescription = document.querySelector("input[name='description']").value;

//     // Perform form validation if needed

//     // Submit the form using AJAX or fetch
//     fetch('/add', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ itemName: itemName, itemPrice: itemPrice, itemDescription: itemDescription }),
//     })
//         .then(response => response.json())
//         .then(data => {
//             console.log('Success:', data);
//             // Optionally, display a success message or redirect to another page
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//             // Handle error scenarios
//         });

//     // Optionally, hide the form after submission
//     var addItemForm = document.getElementById("addItemForm");
//     addItemForm.style.display = "none";
// }


    // Function to toggle section visibility
    function toggleSection(sectionId) {
        var section = document.getElementById(sectionId);
        var sections = document.getElementsByClassName("category-content");

        // Hide all sections except the one with the provided ID
        for (var i = 0; i < sections.length; i++) {
            if (sections[i].id === sectionId) {
                sections[i].style.display = (sections[i].style.display === "none" || sections[i].style.display === "") ? "block" : "none";
            } else {
                sections[i].style.display = "none";
            }
        }
    }



    function toggleFormVisibility() {
        var form = document.getElementById("addItemForm");
        var button = document.querySelector("#puja-samagri .edit-btn");
        if (form.style.display === "none" || form.style.display === "") {
            form.style.display = "block";
            button.textContent = "Close";
        } else {
            form.style.display = "none";
            button.textContent = "Add new Puja Samagri";
        }
    }


    // Function to toggle form visibility for adding Puja Service and change button text
    function toggleServiceFormVisibility() {
        var form = document.getElementById("addServiceForm");
        var button = document.getElementById("toggleServiceFormBtn");
        if (form.style.display === "none") {
            form.style.display = "block";
            button.textContent = "Close";
        } else {
            form.style.display = "none";
            button.textContent = "Add new Puja Service";
        }
    }
    

    // Event listener for the "Add new Puja Service" button
    document.getElementById("toggleServiceFormBtn").addEventListener("click", toggleServiceFormVisibility);


    // temple 

    function toggleFormTemple() {
        var form = document.getElementById("addTempleForm");
        var button = document.getElementById("toggleTempleFormBtn");
        if (form.style.display === "none" || form.style.display === "") {
            form.style.display = "block";
            button.textContent = "Close";
        } else {
            form.style.display = "none";
            button.textContent = "Add Temple";
        }
    }


    // prasadam

    function togglePrasadamForm() {
        var form = document.getElementById("addFormPrasadam");
        var button = document.getElementById("togglePrasadamFormBtn");
        if (form.style.display === "none" || form.style.display === "") {
            form.style.display = "block";
            button.textContent = "Close";
        } else {
            form.style.display = "none";
            button.textContent = "Add new Prasadam";
        }
    }


       
    