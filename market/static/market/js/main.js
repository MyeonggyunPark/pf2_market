// Run the script only after the DOM tree has fully loaded
document.addEventListener("DOMContentLoaded", () => {

  // Mapping between file input IDs and corresponding filename display span IDs
  const files = [
    { input: "id_item_image1", output: "file-name-1" },
    { input: "id_item_image2", output: "file-name-2" },
    { input: "id_item_image3", output: "file-name-3" },
  ];

  // For each file input → output span pair
  files.forEach((f) => {

    // Get the input element and the span where the file name will be shown
    const input = document.getElementById(f.input);
    const output = document.getElementById(f.output);

    // Only attach the listener if the input exists on the current page
    if (input) {

      // When the user selects or clears a file
      input.addEventListener("change", () => {

        // If at least one file is selected, show its name
        if (input.files.length > 0) {
          output.textContent = input.files[0].name;
          output.classList.remove("hidden");
        } else {
          
          // If no file is selected, hide and clear the filename text
          output.textContent = "";
          output.classList.add("hidden");
        }
      });
    }
  });
});
