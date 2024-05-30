// prasadam popup 

function submitQuantity() {
    // Retrieve the entered quantity
    var quantity = document.getElementById('quantityInput').value;
    
    // Perform actions with the quantity (e.g., send it to the server)
    console.log("Quantity entered:", quantity);
    
    // Close the modal
    var modal = document.getElementById('orderPrasadamPopup{{i[0]}}');
    modal.style.display = "none";
    modal.classList.remove('show');
    document.body.classList.remove('modal-open');
    var backdrop = document.getElementsByClassName('modal-backdrop')[0];
    backdrop.parentNode.removeChild(backdrop);
}