// navigation.js

document.addEventListener("DOMContentLoaded", function () {
  const navLinks = {
    "Certificates": "certificates.html",
    "Support": "support.html",
    "About": "about.html",
    "Login": "login.html",
    "Installation Guides": "installation-guides.html",
    "Contact Support": "support.html",
    "Help Center": "support.html",
    "Status Page": "support.html",
    "About Us": "about.html",
    "Privacy Policy": "privacy-policy.html",
    "Terms of Service": "privacy-policy.html",
    "Contact": "support.html"
  };

  document.querySelectorAll("a").forEach((link) => {
    const text = link.innerText.trim();
    if (navLinks[text]) {
      link.href = navLinks[text];
    }
  });

  // Link for Login button
  const loginButton = document.querySelector("button.btn-outline");
  if (loginButton) {
    loginButton.addEventListener("click", function () {
      window.location.href = "login.html";
    });
  }

  // Link for "Get Started Now" button
  const getStartedButton = document.querySelector(".btn-green");
  if (getStartedButton) {
    getStartedButton.addEventListener("click", function () {
      window.location.href = "signup.html";
    });
  }

  // Feature buttons
  const featureButtons = document.querySelectorAll(".card .btn-outline");
  const featurePages = [
    "domain-verification.html",
    "organization-validation.html",
    "certificate-generator.html"
  ];

  featureButtons.forEach((btn, i) => {
    btn.addEventListener("click", () => {
      window.location.href = featurePages[i];
    });
  });
});
