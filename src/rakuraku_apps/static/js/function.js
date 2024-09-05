document.addEventListener("DOMContentLoaded", function () {
    // Function to toggle the display of an accordion content
    function toggleAccordion(button) {
        var panel = button.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    }

    // Get all accordion buttons
    var acc = document.querySelectorAll(".accordion-button");
    acc.forEach(function (button) {
        button.addEventListener("click", function () {
            toggleAccordion(this);
        });
    });
});
