(() => {
  const object = document.getElementById('personal-logo');
  const toggle = document.getElementById('logo-toggle');
  if (!object || !toggle) return;

  let light = false;
  function updateLogo() {
    const svg = object.contentDocument?.documentElement;
    if (svg?.localName === 'svg') {
      svg.style.setProperty('--ink', light ? '#500000' : '#ffffff');
      svg.style.setProperty('--paper', light ? '#ffffff' : '#500000');
      svg.style.setProperty('--blue', light ? '#500000' : '#ffffff');
    }
    toggle.setAttribute('aria-pressed', String(light));
    const label = `Switch logo to ${light ? 'dark' : 'light'} version`;
    toggle.setAttribute('aria-label', label);
    toggle.title = label;
  }

  object.addEventListener('load', updateLogo);
  toggle.addEventListener('click', () => {
    light = !light;
    updateLogo();
  });
  updateLogo();
})();
