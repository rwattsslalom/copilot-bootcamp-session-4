document.addEventListener("DOMContentLoaded", () => {
  const capabilitiesList = document.getElementById("capabilities-list");
  const consultantsList = document.getElementById("consultants-list");
  const capabilitySelect = document.getElementById("capability");
  const consultantSelect = document.getElementById("consultant-registration");
  const registerForm = document.getElementById("register-form");
  const consultantForm = document.getElementById("consultant-form");
  const consultantSubmit = document.getElementById("consultant-submit");
  const consultantCancel = document.getElementById("consultant-cancel");
  const messageDiv = document.getElementById("message");
  let consultantInEdit = null;

  function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = type;
    messageDiv.classList.remove("hidden");

    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  function resetConsultantForm() {
    consultantForm.reset();
    consultantInEdit = null;
    document.getElementById("consultant-email").disabled = false;
    consultantSubmit.textContent = "Create Consultant";
    consultantCancel.classList.add("hidden");
  }

  function populateConsultantForm(consultant) {
    consultantInEdit = consultant.email;
    document.getElementById("consultant-name").value = consultant.name;
    document.getElementById("consultant-email").value = consultant.email;
    document.getElementById("consultant-email").disabled = true;
    document.getElementById("consultant-practice-area").value = consultant.practice_area;
    document.getElementById("consultant-location").value = consultant.location;
    document.getElementById("consultant-bio").value = consultant.bio;
    document.getElementById("consultant-contact-details").value = consultant.contact_details || "";
    consultantSubmit.textContent = "Update Consultant";
    consultantCancel.classList.remove("hidden");
  }

  function renderConsultants(consultants) {
    consultantsList.innerHTML = "";
    consultantSelect.innerHTML = '<option value="">-- Select a consultant --</option>';

    if (consultants.length === 0) {
      consultantsList.innerHTML = "<p><em>No consultants created yet</em></p>";
      return;
    }

    consultants.forEach((consultant) => {
      const card = document.createElement("div");
      card.className = "consultant-card";
      card.innerHTML = `
        <div class="consultant-card-header">
          <div>
            <h4>${consultant.name}</h4>
            <p class="consultant-meta">${consultant.practice_area} • ${consultant.location}</p>
          </div>
          <button type="button" class="edit-btn" data-email="${consultant.email}">Edit</button>
        </div>
        <p class="consultant-email-line">${consultant.email}</p>
        <p>${consultant.bio}</p>
        <p><strong>Contact:</strong> ${consultant.contact_details || "Not provided"}</p>
      `;
      consultantsList.appendChild(card);

      const option = document.createElement("option");
      option.value = consultant.email;
      option.textContent = `${consultant.name} (${consultant.email})`;
      consultantSelect.appendChild(option);
    });

    document.querySelectorAll(".edit-btn").forEach((button) => {
      button.addEventListener("click", async () => {
        const email = button.getAttribute("data-email");
        const response = await fetch(`/consultants/${encodeURIComponent(email)}`);
        const consultant = await response.json();
        populateConsultantForm(consultant);
      });
    });
  }

  // Function to fetch capabilities from API
  async function fetchCapabilities() {
    try {
      const response = await fetch("/capabilities");
      const capabilities = await response.json();

      // Clear loading message
      capabilitiesList.innerHTML = "";
      capabilitySelect.innerHTML = '<option value="">-- Select a capability --</option>';

      // Populate capabilities list
      Object.entries(capabilities).forEach(([name, details]) => {
        const capabilityCard = document.createElement("div");
        capabilityCard.className = "capability-card";

        const availableCapacity = details.capacity || 0;
        const currentConsultants = details.consultants ? details.consultants.length : 0;

        // Create consultants HTML with delete icons
        const consultantsHTML =
          details.consultants && details.consultants.length > 0
            ? `<div class="consultants-section">
              <h5>Registered Consultants:</h5>
              <ul class="consultants-list">
                ${details.consultants
                  .map(
                    (consultant) =>
                      `<li>
                        <div class="consultant-summary">
                          <span class="consultant-email">${consultant.name}</span>
                          <span class="consultant-subtitle">${consultant.email} • ${consultant.practice_area}</span>
                        </div>
                        <button class="delete-btn" data-capability="${name}" data-email="${consultant.email}">Remove</button>
                      </li>`
                  )
                  .join("")}
              </ul>
            </div>`
            : `<p><em>No consultants registered yet</em></p>`;

        capabilityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Practice Area:</strong> ${details.practice_area}</p>
          <p><strong>Industry Verticals:</strong> ${details.industry_verticals ? details.industry_verticals.join(', ') : 'Not specified'}</p>
          <p><strong>Capacity:</strong> ${availableCapacity} hours/week available</p>
          <p><strong>Current Team:</strong> ${currentConsultants} consultants</p>
          <div class="consultants-container">
            ${consultantsHTML}
          </div>
        `;

        capabilitiesList.appendChild(capabilityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        capabilitySelect.appendChild(option);
      });

      // Add event listeners to delete buttons
      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });
    } catch (error) {
      capabilitiesList.innerHTML =
        "<p>Failed to load capabilities. Please try again later.</p>";
      console.error("Error fetching capabilities:", error);
    }
  }

  async function fetchConsultants() {
    try {
      const response = await fetch("/consultants");
      const consultants = await response.json();
      renderConsultants(consultants);
    } catch (error) {
      consultantsList.innerHTML =
        "<p>Failed to load consultants. Please try again later.</p>";
      console.error("Error fetching consultants:", error);
    }
  }

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const capability = button.getAttribute("data-capability");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(
          capability
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");

        // Refresh capabilities list to show updated consultants
        fetchCapabilities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to unregister. Please try again.", "error");
      console.error("Error unregistering:", error);
    }
  }

  consultantForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const consultantPayload = {
      name: document.getElementById("consultant-name").value,
      email: document.getElementById("consultant-email").value,
      practice_area: document.getElementById("consultant-practice-area").value,
      location: document.getElementById("consultant-location").value,
      bio: document.getElementById("consultant-bio").value,
      contact_details: document.getElementById("consultant-contact-details").value || null,
    };

    const isEdit = Boolean(consultantInEdit);
    const endpoint = isEdit
      ? `/consultants/${encodeURIComponent(consultantInEdit)}`
      : "/consultants";
    const method = isEdit ? "PUT" : "POST";
    const body = isEdit
      ? JSON.stringify({
          name: consultantPayload.name,
          practice_area: consultantPayload.practice_area,
          location: consultantPayload.location,
          bio: consultantPayload.bio,
          contact_details: consultantPayload.contact_details,
        })
      : JSON.stringify(consultantPayload);

    try {
      const response = await fetch(endpoint, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body,
      });
      const result = await response.json();

      if (!response.ok) {
        showMessage(result.detail || "Failed to save consultant.", "error");
        return;
      }

      resetConsultantForm();
      fetchConsultants();
      showMessage(
        isEdit
          ? `Updated consultant profile for ${result.name}.`
          : `Created consultant profile for ${result.name}.`,
        "success"
      );
    } catch (error) {
      showMessage("Failed to save consultant. Please try again.", "error");
      console.error("Error saving consultant:", error);
    }
  });

  consultantCancel.addEventListener("click", () => {
    resetConsultantForm();
  });

  // Handle form submission
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = consultantSelect.value;
    const capability = document.getElementById("capability").value;

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(
          capability
        )}/register?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        registerForm.reset();

        // Refresh capabilities list to show updated consultants
        fetchCapabilities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to register. Please try again.", "error");
      console.error("Error registering:", error);
    }
  });

  // Initialize app
  fetchCapabilities();
  fetchConsultants();
  resetConsultantForm();
});
