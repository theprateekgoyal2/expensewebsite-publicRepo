document.addEventListener("DOMContentLoaded", function () {
    // Get references to the button and form elements
    const addButton = document.getElementById("add-source-button");
    const sourceForm = document.getElementById("add-source-form");
    const cancelButton = document.getElementById("cancel-source");

    // When the "Add Source" button is clicked, show the form and hide the button
    addButton.addEventListener("click", function () {
        sourceForm.style.display = "block";
        addButton.style.display = "none";
    });

    // When the "Cancel" button is clicked, hide the form and show the "Add Source" button
    cancelButton.addEventListener("click", function () {
        sourceForm.style.display = "none";
        addButton.style.display = "block";
    });
});
