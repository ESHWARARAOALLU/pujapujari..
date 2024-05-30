function enableEdit() {
    var nameField = document.getElementById('name');
    var emailField = document.getElementById('email');
    var locationField = document.getElementById('location');
    var contactField = document.getElementById('contact');
    var updateBtn = document.getElementById('updateBtn');

    nameField.disabled = false;
    emailField.disabled = false;
    locationField.disabled = false;
    contactField.disabled = false;

    updateBtn.innerText = 'Update';
    updateBtn.setAttribute('onclick', 'saveChanges()');
}

function saveChanges() {
    var nameField = document.getElementById('name');
    var emailField = document.getElementById('email');
    var locationField = document.getElementById('location');
    var contactField = document.getElementById('contact');
    var updateBtn = document.getElementById('updateBtn');

    nameField.disabled = true;
    emailField.disabled = true;
    locationField.disabled = true;
    contactField.disabled = true;

    updateBtn.innerText = 'Edit';
    updateBtn.setAttribute('onclick', 'enableEdit()');
}

// accept and reject alerts 

function acceptRequest() {
    // Perform actions for accepting the request
    alert('Request accepted!');
}

function denyRequest() {
    // Perform actions for denying the request
    alert('Request denied!');
}