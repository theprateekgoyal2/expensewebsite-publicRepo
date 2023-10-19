document.addEventListener("DOMContentLoaded", function () {
    // Get references to the button and form elements
    const addButton = document.getElementById("add-category-button");
    const categoryForm = document.getElementById("add-category-form");
    const cancelButton = document.getElementById("cancel-category");

    // When the "Add Category" button is clicked, show the form and hide the button
    addButton.addEventListener("click", function () {
        categoryForm.style.display = "block";
        addButton.style.display = "none";
    });

    // When the "Cancel" button is clicked, hide the form and show the "Add Category" button
    cancelButton.addEventListener("click", function () {
        categoryForm.style.display = "none";
        addButton.style.display = "block";
    });
});
