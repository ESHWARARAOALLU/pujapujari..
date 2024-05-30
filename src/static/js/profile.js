function toggleOrders() {
    var ordersContainer = document.getElementById('ordersContainer');
    var viewOrdersBtn = document.getElementById('viewOrdersBtn');

    if (ordersContainer.style.display === 'none') {
        ordersContainer.style.display = 'block';
        viewOrdersBtn.textContent = 'Close Orders';
    } else {
        ordersContainer.style.display = 'none';
        viewOrdersBtn.textContent = 'View Orders';
    }
}

function toggleSaveAddress() {
    var addressContainer = document.getElementById('addressContainer');
    var saveAddressBtn = document.getElementById('saveAddressBtn');

    if (addressContainer.style.display === 'none') {
        addressContainer.style.display = 'block';
        saveAddressBtn.textContent = 'Close Address Form';
    } else {
        addressContainer.style.display = 'none';
        saveAddressBtn.textContent = 'Save Address';
    }
}

// profile update and view orders 

function toggleEdit() {
    var nameInput = document.getElementById('name');
    var emailInput = document.getElementById('email');
    var contactInput = document.getElementById('contact');
    var addressInput = document.getElementById('address');
    var updateBtn = document.getElementById('updateProfileBtn');

    if (nameInput.disabled) {
        nameInput.disabled = false;
        emailInput.disabled = false;
        contactInput.disabled = false;
        addressInput.disabled = false;
        updateBtn.innerText = "Save Changes";
    } else {
        // Save changes logic here
        // You can send updated details to the server using AJAX

        // After saving changes, disable inputs again
        nameInput.disabled = true;
        emailInput.disabled = true;
        contactInput.disabled = true;
        addressInput.disabled = true;
        updateBtn.innerText = "Update Profile";
    }
}