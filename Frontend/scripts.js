// scripts.js - final version of routing logic

document.addEventListener("DOMContentLoaded", function () {
  // Logo or Text - Homepage
  const logo = document.querySelector(".header-logo-icon");
  const logoText = document.querySelector(".header-logo-text");

  [logo, logoText].forEach((el) => {
    if (el) {
      el.style.cursor = "pointer";
      el.addEventListener("click", () => {
        window.location.href = "homepage.html";
      });
    }
  });

  // Header Navigation
  document.querySelectorAll("nav a").forEach((navLink) => {
    const text = navLink.textContent.trim().toLowerCase();
    switch (text) {
      case "certificates":
        navLink.href = "certificates.html";
        break;
      case "support":
        navLink.href = "support.html";
        break;
      case "about":
        navLink.href = "about.html";
        break;
    }
  });

  const loginButton = document.querySelector(".btn-outline");
  if (loginButton) {
    loginButton.addEventListener("click", () => {
      window.location.href = "login.html";
    });
  }

  // Next Step - domain input → signup
  const domainInput = document.getElementById("domain");
  const nextStepBtn = domainInput?.nextElementSibling;
  if (nextStepBtn) {
    nextStepBtn.addEventListener("click", () => {
      const domain = domainInput.value.trim();
      if (domain === "") {
        alert("Please enter your domain name.");
      } else {
        window.location.href = "signup.html";
      }
    });
  }

  // Get Started Now Button → signup
  const ctaButtons = Array.from(document.querySelectorAll(".btn-green"));
  const getStartedBtn = ctaButtons.find((btn) => btn.textContent.includes("Get Started Now"));
  if (getStartedBtn) {
    getStartedBtn.addEventListener("click", () => {
      window.location.href = "signup.html";
    });
  }

  // Learn More Buttons → certificates.html
  document.querySelectorAll(".btn-outline").forEach((btn) => {
    if (btn.textContent.includes("Learn More")) {
      btn.addEventListener("click", () => {
        window.location.href = "certificates.html";
      });
    }
  });

  // Footer Links
  document.querySelectorAll("footer a").forEach((link) => {
    const text = link.textContent.trim().toLowerCase();
    if (text.includes("ssl") || text.includes("code signing") || text.includes("multi-domain")) {
      link.href = "certificates.html";
    } else if (text.includes("installation") || text.includes("support") || text.includes("help")) {
      link.href = "support.html";
    } else if (text.includes("about") || text.includes("company") || text.includes("privacy") || text.includes("terms")) {
      link.href = "about.html";
    }
  });
});

