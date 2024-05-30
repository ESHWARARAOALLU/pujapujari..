
function increaseValue(btn) {
    var input = btn.parentElement.previousElementSibling;
    var value = parseInt(input.value, 10);
    value = isNaN(value) ? 1 : value;
    input.value = value + 1;
}

function removeRow(btn) {
    var row = btn.closest("tr");
    row.remove();
}


