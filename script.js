const toggleButton = document.getElementById('dark-mode-toggle');
const body = document.body;


function setActive(clickedButton) {
  // Remove active class from all buttons except dark mode toggle
  const buttons = document.querySelectorAll('nav button:not(#dark-mode-toggle)');
  buttons.forEach(btn => btn.classList.remove('active'));

  // Add active class to clicked button
  clickedButton.classList.add('active');
}

function setActive(btn) {
  // Set active class for nav buttons
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('dark-mode', 'enabled');
  } else {
    localStorage.setItem('dark-mode', 'disabled');
  }
}

// On page load, apply dark mode if enabled and update footer
window.addEventListener('DOMContentLoaded', function() {
  if (localStorage.getItem('dark-mode') === 'enabled') {
    document.body.classList.add('dark-mode');
  }
  const year = document.getElementById('copyright-year');
  if (year) {
    year.textContent = new Date().getFullYear();
  }
  const lastUpdate = document.getElementById('last-update');
  if (lastUpdate) {
    const date = new Date(document.lastModified);
    lastUpdate.textContent = date.toLocaleString('default', { month: 'long', year: 'numeric' });
  }
});
