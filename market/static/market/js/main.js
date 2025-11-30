// Immediately-Invoked Function Expression to avoid leaking variables into global scope
(function () {

  // Run the script only after the DOM tree has fully loaded
  document.addEventListener("DOMContentLoaded", () => {

    // Initialize file name preview behavior for file inputs
    initFileNamePreviews();

    // Initialize custom dropdown UI for item condition selection
    initConditionDropdowns();

    // Keep "sold" toggle in sync between desktop and mobile inputs
    initSoldToggleSync();

    // Initialize AJAX behavior for like buttons
    initLikeButtons();
  });

  // Set up logic for displaying selected file names next to file inputs
  function initFileNamePreviews() {

    // Mapping between file input IDs and corresponding filename display span IDs
    const files = [
      { input: "id_item_image1", output: "file-name-1" },
      { input: "id_item_image2", output: "file-name-2" },
      { input: "id_item_image3", output: "file-name-3" },
      { input: "id_profile_pic", output: "profile-file-name" },
    ];

    // For each file input -> output span pair
    files.forEach(({ input, output }) => {
      const inputEl = document.getElementById(input);
      const outputEl = document.getElementById(output);

      // Only attach the listener if the input exists on the current page
      if (!inputEl || !outputEl) return;

      // When the user selects or clears a file
      inputEl.addEventListener("change", () => {
        const file = inputEl.files[0];

        // If at least one file is selected, show its name
        if (file) {
          outputEl.textContent = file.name;
          outputEl.classList.remove("hidden");
        } else {
          // If no file is selected, hide and clear the filename text
          outputEl.textContent = "";
          outputEl.classList.add("hidden");
        }
      });
    });
  }

  // Set up custom dropdowns for item condition that are backed by radio inputs
  function initConditionDropdowns() {

    // Find all dropdown root elements that manage condition selection
    const dropdownRoots = Array.from(
      document.querySelectorAll("[data-condition-dropdown]")
    );
    if (!dropdownRoots.length) return;

    // Underlying radio buttons that actually store the condition value in the form
    const radios = Array.from(
      document.querySelectorAll('input[name="item_condition"]')
    );
    if (!radios.length) return;

    dropdownRoots.forEach((root) => {
      const trigger = root.querySelector("[data-condition-trigger]");
      const labelSpan = root.querySelector("[data-condition-label]");
      const menu = root.querySelector("[data-condition-menu]");
      const options = root.querySelectorAll("[data-condition-option]");

      // Abort if essential elements are missing
      if (!trigger || !labelSpan || !menu || !options.length) return;

      // Set the visible label based on whichever radio is currently checked
      const setLabelFromChecked = () => {
        const current = radios.find((r) => r.checked);
        if (!current) return;

        options.forEach((opt) => {
          if (opt.dataset.value === current.value) {
            labelSpan.textContent = opt.dataset.label;
          }
        });
      };

      // Initialize dropdown label on page load
      setLabelFromChecked();

      // Toggle menu visibility when clicking the trigger
      trigger.addEventListener("click", (event) => {

        // Prevent click from bubbling up so outer handlers don't immediately close it
        event.stopPropagation();
        menu.classList.toggle("hidden");
      });

      // When user clicks an option, sync radios and close the menu
      options.forEach((opt) => {
        opt.addEventListener("click", () => {
          const { value, label } = opt.dataset;

          // Update the underlying radio buttons
          radios.forEach((r) => {
            r.checked = r.value === value;
          });

          // Update the visible label and hide the menu
          labelSpan.textContent = label;
          menu.classList.add("hidden");
        });
      });
    });

    // Close any open condition dropdowns when clicking outside
    document.addEventListener("click", (event) => {
      dropdownRoots.forEach((root) => {
        const menu = root.querySelector("[data-condition-menu]");
        if (!menu) return;

        if (!root.contains(event.target)) {
          menu.classList.add("hidden");
        }
      });
    });
  }

  // Keep the "sold" state in sync between real form input and mobile-specific toggle
  function initSoldToggleSync() {

    // Actual form input that is submitted
    const realSold = document.querySelector('input[data-sold-real="true"]');

    // Separate input used in mobile UI
    const mobileSold = document.querySelector('input[data-sold-mobile="true"]');

    // Abort if either toggle is missing on the current page
    if (!realSold || !mobileSold) return;

    // Initialize mobile toggle state based on real input
    mobileSold.checked = realSold.checked;

    // When mobile toggle changes, sync the real input
    mobileSold.addEventListener("change", () => {
      realSold.checked = mobileSold.checked;
    });

    // When real input changes (e.g. desktop UI), sync the mobile toggle
    realSold.addEventListener("change", () => {
      mobileSold.checked = realSold.checked;
    });
  }

  // Set up AJAX behavior for like buttons (posts & comments)
  // Handles click events to toggle likes without page reload
  // and updates the heart icon and count text based on the server response.
  function initLikeButtons() {

    // Find all like buttons on the page
    const likeButtons = document.querySelectorAll(".like-btn");

    likeButtons.forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        e.preventDefault(); // Prevent default button behavior

        const url = btn.dataset.url;
        const icon = btn.querySelector(".like-icon");
        const countSpan = btn.querySelector(".like-count");

        try {
          // Send POST request to toggle like status
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token for security
              "Content-Type": "application/json",
            },
          });

          // Handle unauthorized access (e.g., user not logged in)
          if (response.status === 403) {
            window.location.href = "/accounts/login/";
            return;
          }

          if (response.ok) {
            const data = await response.json();

            // Logic 1. Heart Icon Style
            // Toggles the 'fill' class to show filled or empty heart state.
            if (data.liked) {
              icon.classList.remove("fill-none");
              icon.classList.add("fill-current");
            } else {
              icon.classList.remove("fill-current");
              icon.classList.add("fill-none");
            }

            // Logic 2. Count Text Style
            // Updates the count number and toggles text color/weight based on count value.
            countSpan.textContent = data.like_count;

            if (data.like_count > 0) {
              countSpan.classList.remove("text-box-border");
              countSpan.classList.add("text-button-bg");
            } else {
              countSpan.classList.remove("text-button-bg");
              countSpan.classList.add("text-box-border");
            }
          }
        } catch (error) {
          console.error("Error:", error);
        }
      });
    });
  }

  // Tab switching logic for Profile page
  // - Toggles visibility of content sections (Listings/Likes/Comments)
  // - Updates tab button styles (border, text color, icon color)
  function switchTab(tabName) {
    // 1. Hide all content sections
    document
      .querySelectorAll(".tab-content")
      .forEach((el) => el.classList.add("hidden"));

    // 2. Show the selected content
    const targetContent = document.getElementById(`content-${tabName}`);
    if (targetContent) targetContent.classList.remove("hidden");

    // 3. Reset all tab buttons to inactive style
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      // Remove active classes
      btn.classList.remove("border-button-bg", "text-text-main");

      // Add inactive classes
      btn.classList.add(
        "border-transparent",
        "text-site-footer-text",
        "hover:text-button-bg"
      );

      // Reset SVG colors to inactive (Gray with Hover Purple)
      const paths = btn.querySelectorAll(".js-icon-fill");
      const strokes = btn.querySelectorAll(".js-icon-stroke");

      paths.forEach((p) => {
        p.classList.remove("fill-button-bg");
        p.classList.add("fill-site-footer-text", "group-hover:fill-button-bg");
      });

      strokes.forEach((s) => {
        s.classList.remove("stroke-button-bg");
        s.classList.add(
          "stroke-site-footer-text",
          "group-hover:stroke-button-bg"
        );
      });
    });

    // 4. Set active style for clicked button
    const activeBtn = document.getElementById(`tab-btn-${tabName}`);
    if (activeBtn) {
      // Active: Remove inactive & hover classes (Disable hover effect)
      activeBtn.classList.remove(
        "border-transparent",
        "text-site-footer-text",
        "hover:text-button-bg"
      );
      // Add active classes
      activeBtn.classList.add("border-button-bg", "text-text-main");

      // Set SVG colors to active (Purple) & Remove group-hover classes
      const activePaths = activeBtn.querySelectorAll(".js-icon-fill");
      const activeStrokes = activeBtn.querySelectorAll(".js-icon-stroke");

      activePaths.forEach((p) => {
        p.classList.remove(
          "fill-site-footer-text",
          "group-hover:fill-button-bg"
        );
        p.classList.add("fill-button-bg");
      });

      activeStrokes.forEach((s) => {
        s.classList.remove(
          "stroke-site-footer-text",
          "group-hover:stroke-button-bg"
        );
        s.classList.add("stroke-button-bg");
      });
    }
  }

  // Toggle visibility between view mode and edit form for a comment
  function toggleCommentEdit(commentId) {
    const viewMode = document.getElementById(`comment-view-${commentId}`);
    const editMode = document.getElementById(`comment-edit-${commentId}`);

    if (viewMode && editMode) {
      viewMode.classList.toggle("hidden");
      editMode.classList.toggle("hidden");
    }
  }

  // Open the delete confirmation modal and set the form action URL dynamically
  function openDeleteModal(deleteUrl) {
    const modal = document.getElementById("delete-modal");
    const form = document.getElementById("delete-form");

    // Set the action URL so the form submits to the correct endpoint
    if (form) form.action = deleteUrl;

    // Display the modal
    if (modal) modal.classList.remove("hidden");
  }

  // Close the delete confirmation modal
  function closeDeleteModal() {
    const modal = document.getElementById("delete-modal");
    if (modal) modal.classList.add("hidden");
  }

  // Helper function to retrieve the CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // [GLOBAL EXPOSURE]
  // Explicitly expose functions to the global 'window' object
  // so they can be called from HTML event handlers (onclick="...")
  window.switchTab = switchTab;
  window.toggleCommentEdit = toggleCommentEdit;
  window.openDeleteModal = openDeleteModal;
  window.closeDeleteModal = closeDeleteModal;
})();