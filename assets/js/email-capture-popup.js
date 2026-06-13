(function () {
  "use strict";

  var COOKIE_NAME = "bwo_popup_shown";
  var COOKIE_DAYS = 7;
  var DELAY_MS = 60000;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie =
      name + "=" + value + ";expires=" + d.toUTCString() + ";path=/;SameSite=Lax";
  }

  if (getCookie(COOKIE_NAME)) return;

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  var popupEl = null;
  var overlayEl = null;
  var styleEl = null;
  var shown = false;
  var triggered = false;

  function cleanup() {
    if (popupEl && popupEl.parentNode) popupEl.parentNode.removeChild(popupEl);
    if (overlayEl && overlayEl.parentNode)
      overlayEl.parentNode.removeChild(overlayEl);
    if (styleEl && styleEl.parentNode) styleEl.parentNode.removeChild(styleEl);
    popupEl = null;
    overlayEl = null;
    styleEl = null;
  }

  function hidePopup() {
    if (!shown) return;
    shown = false;
    popupEl.style.opacity = "0";
    popupEl.style.transform = "translateY(20px)";
    overlayEl.style.opacity = "0";
    setTimeout(cleanup, 300);
  }

  function onSubmit(e) {
    e.preventDefault();
    var input = document.getElementById("bwo-email-input");
    var btn = document.getElementById("bwo-email-btn");
    var email = input.value.trim();
    if (!isValidEmail(email)) {
      input.style.borderColor = "#c0392b";
      return;
    }
    input.style.borderColor = "rgba(201, 191, 176, 0.5)";
    btn.disabled = true;
    btn.textContent = "Sending...";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://thinksmart.life/forms/brentwoodorganizers/lead-capture", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function () {
      if (typeof gtag === "function") {
        gtag("event", "popup_submit", {
          popup_name: "email_capture",
          source_page: window.location.pathname,
        });
      }
      btn.textContent = "\u2713 Sent!";
      setTimeout(function () {
        hidePopup();
      }, 1500);
    };
    xhr.onerror = function () {
      if (typeof gtag === "function") {
        gtag("event", "popup_submit", {
          popup_name: "email_capture",
          source_page: window.location.pathname,
        });
      }
      btn.textContent = "\u2713 Sent!";
      setTimeout(function () {
        hidePopup();
      }, 1500);
    };
    xhr.send(
      JSON.stringify({
        email: email,
        source_page: window.location.pathname,
      })
    );
  }

  function showPopup() {
    if (triggered) return;
    triggered = true;
    shown = true;

    setCookie(COOKIE_NAME, "1", COOKIE_DAYS);

    if (typeof gtag === "function") {
      gtag("event", "popup_impression", {
        popup_name: "email_capture",
        source_page: window.location.pathname,
      });
    }

    styleEl = document.createElement("style");
    styleEl.textContent = [
      "#bwo-popup-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(42,37,32,0.35);z-index:99998;opacity:0;transition:opacity 0.3s ease;}",
      "#bwo-popup-container{position:fixed;bottom:24px;right:24px;width:380px;max-width:calc(100vw - 32px);background:#faf8f4;border:1px solid rgba(184,150,90,0.18);border-radius:0;padding:28px;z-index:99999;box-shadow:0 24px 70px rgba(42,37,32,0.12);opacity:0;transform:translateY(20px);transition:opacity 0.3s ease,transform 0.3s ease;color:#2a2520;font-family:'Inter',Arial,sans-serif;line-height:1.5;}",
      "#bwo-popup-close{position:absolute;top:12px;right:12px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#9c9289;font-size:20px;border:none;background:none;padding:0;line-height:1;}",
      "#bwo-popup-close:hover{color:#2a2520;}",
      "#bwo-popup-title{font-size:20px;font-weight:400;color:#2a2520;margin:0 0 10px 0;font-family:'Cormorant Garamond',Georgia,serif;letter-spacing:0;}",
      "#bwo-popup-body{font-size:14px;color:rgba(42,37,32,0.65);margin:0 0 18px 0;line-height:1.6;}",
      "#bwo-popup-form{display:flex;gap:8px;}",
      "#bwo-email-input{flex:1;padding:10px 14px;border:1px solid rgba(201,191,176,0.5);border-radius:0;background:#ffffff;color:#2a2520;font-size:14px;font-family:'Inter',Arial,sans-serif;outline:none;}",
      "#bwo-email-input:focus{border-color:#b8965a;box-shadow:0 0 0 3px rgba(184,150,90,0.15);}",
      "#bwo-email-input::placeholder{color:#9c9289;}",
      "#bwo-email-btn{padding:10px 18px;border:none;border-radius:0;background:#2a2520;color:#faf8f4;font-size:14px;font-weight:500;cursor:pointer;white-space:nowrap;font-family:'Inter',Arial,sans-serif;letter-spacing:0.02em;transition:background 0.2s;}",
      "#bwo-email-btn:hover{background:#b8965a;}",
      "#bwo-email-btn:disabled{opacity:0.6;cursor:default;}",
      "#bwo-popup-footer{font-size:12px;color:rgba(42,37,32,0.5);margin-top:14px;}",
      "@media(max-width:599px){#bwo-popup-container{bottom:16px;left:16px;right:16px;width:auto;max-width:none;}}",
    ].join(" ");
    document.head.appendChild(styleEl);

    overlayEl = document.createElement("div");
    overlayEl.id = "bwo-popup-overlay";
    document.body.appendChild(overlayEl);

    popupEl = document.createElement("div");
    popupEl.id = "bwo-popup-container";
    popupEl.innerHTML =
      '<button id="bwo-popup-close">&times;</button>' +
      '<h2 id="bwo-popup-title">Organize your inbox</h2>' +
      '<p id="bwo-popup-body">Get design inspiration, organization tips, and exclusive offers from Brentwood Organizers — delivered to your inbox.</p>' +
      '<form id="bwo-popup-form">' +
      '<input id="bwo-email-input" type="email" placeholder="Your email address" autocomplete="email" required>' +
      '<button id="bwo-email-btn" type="submit">Subscribe</button>' +
      "</form>" +
      '<p id="bwo-popup-footer">No spam. Unsubscribe anytime.</p>';
    document.body.appendChild(popupEl);

    document
      .getElementById("bwo-popup-close")
      .addEventListener("click", hidePopup);
    document.getElementById("bwo-popup-form").addEventListener("submit", onSubmit);
    overlayEl.addEventListener("click", hidePopup);

    requestAnimationFrame(function () {
      popupEl.style.opacity = "1";
      popupEl.style.transform = "translateY(0)";
      overlayEl.style.opacity = "1";
    });
  }

  setTimeout(function () {
    if (!triggered) showPopup();
  }, DELAY_MS);
})();
