const requestForm = document.getElementById("brentwood-contact-form");
const serviceSelect = document.getElementById("service");
const formStatus = document.getElementById("brentwood-form-status");
const calendlyBooking = document.getElementById("calendly-booking");
const calendlyHost = document.getElementById("calendly-inline-host");
const calendlyUrl =
  "https://calendly.com/rhode-brentwoodorganizers/let-s-talk-home-organization-support-clone";
const mediaInput = requestForm
  ? requestForm.querySelector("[data-media-input]")
  : null;
const mediaPreview = requestForm
  ? requestForm.querySelector("[data-media-preview]")
  : null;
const params = new URLSearchParams(window.location.search);
const requestedService = params.get("service");
const maxMediaFiles = 3;
const maxMediaFileSize = 50 * 1024 * 1024;
const allowedMediaTypes = new Set([
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/gif",
  "video/mp4",
  "video/webm",
  "video/quicktime",
]);
let selectedMediaFiles = [];

function formatSize(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function renderSelectedMedia(files) {
  if (!mediaPreview) return;
  mediaPreview.innerHTML = "";
  if (!files || files.length === 0) return;

  Array.from(files).forEach(function (file) {
    const item = document.createElement("div");
    item.className = "media-preview-item";
    item.innerHTML =
      "<span>" +
      file.name +
      "</span><span>" +
      formatSize(file.size) +
      "</span>";
    mediaPreview.appendChild(item);
  });
}

function appendSelectedMedia(newFiles) {
  const nextFiles = selectedMediaFiles.slice();
  Array.from(newFiles || []).forEach(function (file) {
    const key = file.name + "|" + file.size + "|" + file.lastModified;
    const exists = nextFiles.some(function (existing) {
      return (
        existing.name + "|" + existing.size + "|" + existing.lastModified ===
        key
      );
    });
    if (!exists && nextFiles.length < maxMediaFiles) {
      nextFiles.push(file);
    }
  });
  selectedMediaFiles = nextFiles;
}

function getMediaValidationError(files) {
  if (!files || files.length === 0) return "";
  if (files.length > maxMediaFiles) {
    return "Puedes subir hasta " + maxMediaFiles + " archivos.";
  }

  for (const file of files) {
    if (!allowedMediaTypes.has(file.type)) {
      return "Formato de archivo no compatible.";
    }
    if (file.size > maxMediaFileSize) {
      return "Cada archivo debe ser menor de 50 MB.";
    }
  }

  return "";
}

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
  if (mediaInput) {
    mediaInput.addEventListener("change", function () {
      appendSelectedMedia(mediaInput.files);
      renderSelectedMedia(selectedMediaFiles);

      const mediaError = getMediaValidationError(selectedMediaFiles);
      if (mediaError) {
        formStatus.style.display = "block";
        formStatus.style.color = "#dc3545";
        formStatus.textContent = mediaError;
      }

      mediaInput.value = "";
    });
  }

  requestForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = {};
    requestForm
      .querySelectorAll("input, select, textarea")
      .forEach(function (input) {
        if (!input.name) return;
        formData[input.name] = input.value.trim();
      });

    const mediaError = getMediaValidationError(selectedMediaFiles);
    if (mediaError) {
      if (formStatus) {
        formStatus.style.display = "block";
        formStatus.style.color = "#dc3545";
        formStatus.textContent = mediaError;
      }
      return;
    }

    const requestBody = new FormData();
    Object.keys(formData).forEach(function (key) {
      requestBody.append(key, formData[key]);
    });
    selectedMediaFiles.forEach(function (file) {
      requestBody.append("media", file);
    });

    const submitButton = requestForm.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Enviando...";
    }

    if (formStatus) {
      formStatus.style.display = "block";
      formStatus.style.color = "#6b6259";
      formStatus.textContent = "Enviando...";
    }

    fetch("https://thinksmart.life/forms/brentwood/submit", {
      method: "POST",
      body: requestBody,
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
            "¡Gracias! Tu solicitud ha sido recibida. Te contactaremos en breve.";
        }
        if (typeof window.gtag === "function") {
          window.gtag("event", "generate_lead", { method: "contact_form" });
        }
        showCalendly(formData);
        requestForm.reset();
        selectedMediaFiles = [];
        renderSelectedMedia([]);
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
            "Lo sentimos, hubo un problema al enviar tu solicitud. Por favor escríbenos directamente a info@brentwoodorganizers.com o inténtalo de nuevo.";
        }
        console.error("Form submission error:", error);
      })
      .finally(function () {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = "Enviar Solicitud";
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
