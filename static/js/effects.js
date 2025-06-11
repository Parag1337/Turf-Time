document.addEventListener('DOMContentLoaded', function() {
  // Navbar scroll effect
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
      } else {
        navbar.classList.remove('navbar-scrolled');
      }
    });
  }
  
  // Initial scroll check
  if (window.scrollY > 50 && navbar) {
    navbar.classList.add('navbar-scrolled');
  }
  
  // Animate elements as they come into view
  const animateOnScroll = function() {
    const elements = document.querySelectorAll('.slide-up, .fade-right, .fade-left');
    elements.forEach(element => {
      const elementPosition = element.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;
      if (elementPosition < windowHeight - 100) {
        element.classList.add('visible');
      }
    });
  };
  
  // Run once on load
  animateOnScroll();
  
  // Add scroll listener
  window.addEventListener('scroll', animateOnScroll);
  
  // Handle tabbed content
  const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
  tabButtons.forEach(button => {
    button.addEventListener('shown.bs.tab', e => {
      const targetPane = document.querySelector(e.target.getAttribute('data-bs-target'));
      if (targetPane) {
        const animatedElements = targetPane.querySelectorAll('.slide-up, .fade-right, .fade-left');
        animatedElements.forEach(element => {
          element.classList.add('visible');
        });
      }
    });
  });
});