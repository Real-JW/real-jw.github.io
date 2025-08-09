function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');
  localStorage.setItem('dark-mode', body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

function loadComponent(id, url, callback) {
  const container = document.getElementById(id);
  if (container) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        container.innerHTML = html;
        if (callback) callback();
      });
  }
}

window.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('dark-mode') === 'enabled') {
    document.body.classList.add('dark-mode');
  }

  loadComponent('nav-container', 'includes/nav.html', () => {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('#nav-container nav button[data-link]').forEach(btn => {
      const link = btn.getAttribute('data-link');
      btn.addEventListener('click', () => { window.location.href = link; });
      if (link === currentPage) {
        btn.classList.add('active');
      }
    });
    const toggleButton = document.getElementById('dark-mode-toggle');
    if (toggleButton) {
      toggleButton.addEventListener('click', toggleDarkMode);
    }
  });

  loadComponent('footer-container', 'includes/footer.html', () => {
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

  loadComponent('publications-container', 'includes/publications.html');
});
