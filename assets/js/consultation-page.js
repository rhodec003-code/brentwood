const requestForm = document.getElementById("brentwood-contact-form");
const serviceSelect = document.getElementById("service");
const formStatus = document.getElementById("brentwood-form-status");
const calendlyBooking = document.getElementById("calendly-booking");
const calendlyHost = document.getElementById("calendly-inline-host");
const calendlyUrl =
  "https://calendly.com/rhode-brentwoodorganizers/let-s-talk-home-organization-support-clone";
const params = new URLSearchParams(window.location.search);
const requestedService = params.get("service");

function showCalendly(formData) {
  if (!calendlyBooking || !calendlyHost) return;
  calendlyBooking.style.display = "block";

  if (window.Calendly && calendlyHost.dataset.initialized !== "true") {
    window.Calendly.initInlineWidget({
      url: calendlyUrl,
      parentElement: calendlyHost,
      prefill: {
        name: formData["Full Name"] || "",
        email: formData.Email || "",
      },
    });
    calendlyHost.dataset.initialized = "true";
  }

  if (typeof window.gtag === "function") {
    window.gtag("event", "schedule_consultation", {
      method: "calendly_sidebar",
    });
  }

  calendlyBooking.scrollIntoView({ behavior: "smooth", block: "start" });
}

if (requestedService && serviceSelect) {
  const matchingOption = Array.from(serviceSelect.options).find(
    function (option) {
      return (
        option.value === requestedService || option.text === requestedService
      );
    },
  );

  if (matchingOption) {
    serviceSelect.value = matchingOption.value || matchingOption.text;
  }
}

if (requestForm) {
  requestForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = {};
    let isValid = true;
    let firstInvalidField = null;

    requestForm
      .querySelectorAll("input, select, textarea")
      .forEach(function (input) {
        if (!input.name) return;
        const trimmedValue = input.value.trim();
        formData[input.name] = trimmedValue;

        if (input.hasAttribute("required") && trimmedValue === "") {
          isValid = false;
          if (!firstInvalidField) {
            firstInvalidField = input;
          }
        }
      });

    if (!isValid) {
      if (formStatus) {
        formStatus.style.display = "block";
        formStatus.style.color = "#dc3545";
        formStatus.textContent =
          "Please fill in all required fields before submitting.";
      }
      if (firstInvalidField) {
        firstInvalidField.focus();
      }
      return;
    }

    const submitButton = requestForm.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Submitting...";
    }

    if (formStatus) {
      formStatus.style.display = "block";
      formStatus.style.color = "#6b6259";
      formStatus.textContent = "Submitting...";
    }

    fetch("https://thinksmart.life/forms/brentwood/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (result) {
        if (!result.success) {
          throw new Error(result.message || "Submission failed");
        }

        if (formStatus) {
          formStatus.style.color = "#198754";
          formStatus.textContent =
            "Thank you! Your request has been received. We will be in touch shortly.";
        }
        if (typeof window.gtag === "function") {
          window.gtag("event", "generate_lead", { method: "contact_form" });
        }
        showCalendly(formData);
        requestForm.reset();
        if (requestedService && serviceSelect) {
          const matchingOption = Array.from(serviceSelect.options).find(
            function (option) {
              return (
                option.value === requestedService ||
                option.text === requestedService
              );
            },
          );
          if (matchingOption) {
            serviceSelect.value = matchingOption.value || matchingOption.text;
          }
        }
      })
      .catch(function (error) {
        if (formStatus) {
          formStatus.style.color = "#dc3545";
          formStatus.textContent =
            "Sorry, there was a problem submitting your request. Please email us directly at info@brentwoodorganizers.com or try again.";
        }
        console.error("Form submission error:", error);
      })
      .finally(function () {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = "Send Request";
        }
      });
  });
}

(function () {
  const mobileQuery = window.matchMedia("(max-width: 1024px)");
  document.querySelectorAll("nav").forEach(function (nav) {
    const toggle = nav.querySelector(".mobile-menu-toggle");
    const links = nav.querySelector(".nav-links");
    if (!toggle || !links) return;

    toggle.addEventListener("click", function () {
      const isOpen = nav.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });

    nav.querySelectorAll(".nav-item-services > a").forEach(function (trigger) {
      trigger.addEventListener("click", function (event) {
        if (!mobileQuery.matches) return;
        event.preventDefault();
        trigger.parentElement.classList.toggle("dropdown-open");
      });
    });

    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (
          !mobileQuery.matches ||
          link.parentElement.classList.contains("nav-item-services")
        )
          return;
        nav.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  });
})();
