
// Show a welcome message when the homepage loads.
document.addEventListener("DOMContentLoaded", function () {
    console.log("CampusConnect is ready!");

    // Add a message when users click an event button.
    const eventButtons = document.querySelectorAll(".event-button");

    eventButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            alert("Thanks for checking out CampusConnect!");
        });
    });
});

// CampusConnect interactive features
document.addEventListener("DOMContentLoaded", function () {
    console.log("CampusConnect is ready!");

    // Event button interaction
    document.querySelectorAll(".event-button").forEach(function (button) {
        button.addEventListener("click", function () {
            button.textContent = "Interested!";
            button.disabled = true;
        });
    });

    // Load sample campus information
    const loadButton = document.getElementById("loadData");

    if (loadButton) {
        loadButton.addEventListener("click", async function () {
            const results = document.getElementById("apiResults");
            results.textContent = "Loading campus information...";

            try {
                const response = await fetch(
                    "https://jsonplaceholder.typicode.com/posts/1"
                );

                if (!response.ok) {
                    throw new Error("Unable to load data");
                }

                const data = await response.json();

                results.innerHTML = `
                    <h4>${data.title}</h4>
                    <p>${data.body}</p>
                    <p class="text-success">API data loaded successfully!</p>
                `;
            } catch (error) {
                results.textContent = "Could not load data. Please try again.";
            }
        });
    }

    // Demonstration login form
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            document.getElementById("loginMessage").textContent =
                "Login demonstration successful! Authentication is not connected yet.";
        });
    }
});
