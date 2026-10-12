// Content and navigation are generated at build time; JavaScript adds interactions.
function readDarkMode() {
  try {
    return localStorage.getItem('dark-mode') === 'enabled';
  } catch {
    return false;
  }
}

function setDarkMode(enabled) {
  document.body.classList.toggle('dark-mode', enabled);
  document.documentElement.classList.toggle('dark-mode', enabled);
  document.getElementById('dark-mode-toggle')?.setAttribute('aria-pressed', String(enabled));
}

function toggleDarkMode() {
  const enabled = !document.body.classList.contains('dark-mode');
  setDarkMode(enabled);
  try {
    localStorage.setItem('dark-mode', enabled ? 'enabled' : 'disabled');
  } catch {
    // The toggle still works when browser storage is unavailable.
  }
}

window.addEventListener('DOMContentLoaded', () => {
  setDarkMode(readDarkMode());
  document.getElementById('dark-mode-toggle')?.addEventListener('click', toggleDarkMode);
  const year = document.getElementById('copyright-year');
  if (year) year.textContent = new Date().getFullYear();
});
