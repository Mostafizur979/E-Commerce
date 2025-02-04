document.addEventListener("DOMContentLoaded", function () {
    const menuItems = document.querySelectorAll(".profile-hide");
  
    // Function to toggle sub-menu on click
    function toggleSubMenu(event) {
      const subMenu = this.querySelector("ul");
      if (subMenu && !event.target.closest("a")) {
        event.preventDefault();
        event.stopPropagation();
        this.classList.toggle("active");
      }
    }
  
    // Attach click event listener to each menu item
    menuItems.forEach((menuItem) => {
      menuItem.addEventListener("click", toggleSubMenu);
    });
  });
  