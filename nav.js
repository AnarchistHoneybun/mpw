/*
 * Site navigation, theme toggle and mobile menu.
 *
 * Each page loads this with a single <script src="nav.js"></script> tag placed
 * where the <nav> should appear (just inside <body>). The nav markup is built
 * here so there is one source of truth; the link matching the current page is
 * bolded automatically.
 */
(function () {
  "use strict";

  // Apply the saved theme before the rest of the page paints.
  var savedTheme = localStorage.getItem("theme") || "light";
  document.body.setAttribute("data-theme", savedTheme);

  // Work out how deep we are so links resolve from sub-directories too.
  var path = location.pathname;
  var file = path.substring(path.lastIndexOf("/") + 1) || "index.html";
  var inSubdir = /\/(blogposts|projectposts)\//.test(path);
  var prefix = inSubdir ? "../" : "./";

  // Blog/project posts keep their section tab highlighted.
  var active = file;
  if (path.indexOf("/blogposts/") !== -1) active = "blog.html";
  else if (path.indexOf("/projectposts/") !== -1) active = "projects.html";

  var LINKS = [
    ["index.html", "Home"],
    ["blog.html", "Blog"],
    ["projects.html", "Projects"],
    ["oss.html", "OSS"],
    ["journal.html", "Journal"],
    // ["status.html", "Status"], // hidden from public view for now
    // ["botched_hemline.html", "botched_hemline"],
  ];

  var linksHTML = LINKS.map(function (link) {
    var cls = link[0] === active ? ' class="active"' : "";
    return '<a href="' + prefix + link[0] + '"' + cls + ">" + link[1] + "</a>";
  }).join("\n        ");

  var navHTML =
    "<nav>\n" +
    '      <div class="nav-left">\n        ' +
    linksHTML +
    "\n      </div>\n" +
    '      <button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">\n' +
    '        <span class="theme-toggle-text"></span>\n' +
    "      </button>\n" +
    '      <button class="hamburger" id="hamburger" aria-label="Toggle navigation menu"></button>\n' +
    "    </nav>";

  var marker = document.currentScript;
  if (marker) marker.insertAdjacentHTML("afterend", navHTML);
  else document.body.insertAdjacentHTML("afterbegin", navHTML);

  // Theme toggle
  var body = document.body;
  var themeToggle = document.getElementById("theme-toggle");
  var themeText = document.querySelector(".theme-toggle-text");

  function updateText(theme) {
    themeText.textContent = theme === "dark" ? "LIGHT MODE" : "DARK MODE";
  }
  updateText(savedTheme);

  themeToggle.addEventListener("click", function () {
    var next = body.getAttribute("data-theme") === "dark" ? "light" : "dark";
    body.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    updateText(next);
  });

  // Mobile hamburger menu
  var hamburger = document.getElementById("hamburger");
  var navLeft = document.querySelector(".nav-left");

  hamburger.addEventListener("click", function () {
    hamburger.classList.toggle("active");
    navLeft.classList.toggle("active");
  });

  navLeft.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      hamburger.classList.remove("active");
      navLeft.classList.remove("active");
    });
  });

  document.addEventListener("click", function (e) {
    if (
      window.innerWidth <= 768 &&
      !hamburger.contains(e.target) &&
      !navLeft.contains(e.target)
    ) {
      hamburger.classList.remove("active");
      navLeft.classList.remove("active");
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 768) {
      hamburger.classList.remove("active");
      navLeft.classList.remove("active");
    }
  });
})();
