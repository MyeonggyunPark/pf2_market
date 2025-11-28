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

    // For each file input → output span pair
    files.forEach(({ input, output }) => {

      // Get the input element and the span where the file name will be shown
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
      // Trigger button that opens/closes the dropdown
      const trigger = root.querySelector("[data-condition-trigger]");

      // Span displaying the currently selected condition label
      const labelSpan = root.querySelector("[data-condition-label]");

      // Dropdown menu container
      const menu = root.querySelector("[data-condition-menu]");

      // Individual options inside the dropdown menu
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

  // Expose functions to the global window object for HTML event handlers
  
  // Toggle between view mode and edit mode for a specific comment
  window.toggleCommentEdit = function(commentId) {
    const viewMode = document.getElementById(`comment-view-${commentId}`);
    const editMode = document.getElementById(`comment-edit-${commentId}`);
    
    if (viewMode && editMode) {
      viewMode.classList.toggle("hidden");
      editMode.classList.toggle("hidden");
    }
  };

  // Open the delete modal and dynamically set the form action URL
  window.openDeleteModal = function(deleteUrl) {
    const modal = document.getElementById('delete-modal');
    const form = document.getElementById('delete-form');
    
    // Set the action URL for the form to the specific comment's delete URL
    form.action = deleteUrl;
    
    // Show the modal
    modal.classList.remove('hidden');
  };

  // Close the delete modal and hide the overlay
  window.closeDeleteModal = function() {
    const modal = document.getElementById('delete-modal');
    modal.classList.add('hidden');
  };

})();