
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("shoutoutForm");  // Form element
    const shoutoutTableBody = document.getElementById("shoutoutTableBody");  // Table body where shoutouts are displayed

    // Define the base URL for the API
    const BASE_URL = "http://127.0.0.1:3000/api/v1/shoutouts";  // Adjust if needed

    // Fetch shoutouts from the API and render them in the table
    async function fetchShoutouts() {
        try {
            const response = await fetch(BASE_URL);
            const shoutouts = await response.json();
            renderShoutouts(shoutouts);
        } catch (error) {
            console.error("Error fetching shoutouts:", error);
        }
    }

     // Function to render shoutouts in the table
     function renderShoutouts(shoutouts) {
        shoutoutTableBody.innerHTML = ''; // Clear the table body
        shoutouts.forEach(shoutout => {
            console.log(shoutout)
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${shoutout.id}</td>
                <td>${shoutout.Contents}</td>
                <td>${shoutout.CreationTime}</td>
                <td>${shoutout.Likes}</td>
                <td>
                    <div class="actions">
                        <button class="like-btn" onclick="likeShoutout(${shoutout.id})">Like</button>
                        <button class="delete-btn" onclick="deleteShoutout(${shoutout.id})">Delete</button>
                    </div>
                </td>
            `;
            shoutoutTableBody.appendChild(row);
        });
    }
   
    // Handle form submission (POST shoutout)
    form.addEventListener("submit", async function (event) {
        event.preventDefault();  // Prevent the default form submission behavior

        const shoutoutInput = document.getElementById("shoutoutInput").value;
        if (shoutoutInput.trim() !== "") {
            try {
                const response = await fetch(BASE_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ contents: shoutoutInput }),
                });

                if (response.ok) {
                    fetchShoutouts();  // Fetch updated list of shoutouts
                    form.reset();  // Clear the form input
                } else {
                    alert("Failed to add shoutout.");
                }
            } catch (error) {
                console.error("Error posting shoutout:", error);
            }
        }
    });

    // Handle delete shoutout (DELETE request)
    window.deleteShoutout = async function(id) {
    // async function deleteShoutout(id) {
        try {
            const response = await fetch(`${BASE_URL}/${id}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                fetchShoutouts();  // Re-fetch shoutouts after deletion
            } else {
                alert("Failed to delete shoutout.");
            }
        } catch (error) {
            console.error("Error deleting shoutout:", error);
        }
    }
     // Function to handle liking a shoutout
     window.likeShoutout = async function(itemId) {
    //  async function likeShoutout(itemId) {
        const response = await fetch(`${BASE_URL}/like/${itemId}`, {
            method: 'PUT',
        });

        if (response.ok) {
            fetchShoutouts();  // Re-fetch updated items after liking
        } else {
            alert("Failed to like shoutout.");
        }
    }

    // Fetch shoutouts on page load
    fetchShoutouts();
});