document.addEventListener("DOMContentLoaded", function () {
    // Cache DOM elements
    const navLinks = document.querySelectorAll("nav a");
    const contactForm = document.getElementById("contact-form");
    const skillsSection = document.getElementById("skills");
    const sections = document.querySelectorAll("section");
    const navItems = document.querySelectorAll("nav ul li a");
  
    // ========== Smooth Scrolling ==========
    function handleNavClick(e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: "smooth",
        });
      }
    }
  
    navLinks.forEach(anchor => {
      anchor.addEventListener("click", handleNavClick);
    });
  
    // ========== Contact Form ==========
    if (contactForm) {
      const messageDiv = document.getElementById("form-message");
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      
      async function handleFormSubmit(e) {
        e.preventDefault();
        
        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.textContent = "Sending...";
        
        try {
          const formData = new FormData(contactForm);
          const response = await fetch(contactForm.action, {
            method: "POST",
            body: formData,
            headers: { Accept: "application/json" },
          });
  
          if (!response.ok) throw new Error("Network response was not ok");
          
          const data = await response.json();
          
          // Display message
          messageDiv.textContent = data.message;
          messageDiv.className = data.success ? "success" : "error";
          
          if (data.success) contactForm.reset();
          
        } catch (error) {
          console.error("Error:", error);
          messageDiv.textContent = "There was an error sending your message. Please try again.";
          messageDiv.className = "error";
        } finally {
          submitBtn.disabled = false;
          submitBtn.textContent = "Send Message";
          
          // Hide message after 5 seconds
          setTimeout(() => {
            messageDiv.textContent = "";
            messageDiv.className = "";
          }, 5000);
        }
      }
  
      contactForm.addEventListener("submit", handleFormSubmit);
    }
  
    // ========== Skill Bars Animation ==========
    function animateSkillBars() {
      document.querySelectorAll(".skill-level").forEach(bar => {
        const width = bar.style.width;
        bar.style.width = "0";
        setTimeout(() => {
          bar.style.width = width;
        }, 100);
      });
    }
  
    if (skillsSection) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              animateSkillBars();
              observer.unobserve(entry.target);
            }
          });
        }, 
        { threshold: 0.5 }
      );
      observer.observe(skillsSection);
    }
  
    // ========== Active Navigation ==========
    function updateActiveNav() {
      let current = "";
      
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop - 100) {
          current = section.getAttribute("id");
        }
      });
  
      navItems.forEach(item => {
        item.classList.toggle(
          "active", 
          item.getAttribute("href") === `#${current}`
        );
      });
    }
  
    window.addEventListener("scroll", updateActiveNav);
    updateActiveNav(); // Initialize on load
  });