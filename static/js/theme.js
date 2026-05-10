/* ============================================================
   TRAVELOOP — Theme Manager
   Handles light/dark mode with system preference + persistence
   ============================================================ */

const ThemeManager = (() => {
  const STORAGE_KEY = 'traveloop_theme';
  const DARK        = 'dark';
  const LIGHT       = 'light';

  // Read saved preference, fallback to system preference
  function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY);
  }

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? DARK : LIGHT;
  }

  function getCurrentTheme() {
    return getSavedTheme() || getSystemTheme();
  }

  // Apply theme to <html data-bs-theme="...">
  function applyTheme(theme) {
    const html = document.documentElement;
    html.setAttribute('data-bs-theme', theme);
    html.style.colorScheme = theme;     // tells browser scrollbars, inputs etc.

    // Update every toggle button's tooltip
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.setAttribute(
        'data-tooltip',
        theme === DARK ? 'Switch to Light' : 'Switch to Dark'
      );
      btn.setAttribute('aria-label', btn.getAttribute('data-tooltip'));
    });

    // Chart.js global defaults if Chart is loaded
    if (window.Chart) {
      const textColor  = theme === DARK ? '#A8A29E' : '#57534E';
      const gridColor  = theme === DARK ? '#2C2420' : '#E7E5E4';
      Chart.defaults.color       = textColor;
      Chart.defaults.borderColor = gridColor;
    }
  }

  function toggleTheme() {
    const current = getCurrentTheme();
    const next    = current === DARK ? LIGHT : DARK;
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);

    // Ripple animation on toggle
    const btn = document.querySelector('.theme-toggle');
    if (btn) {
      btn.classList.remove('theme-toggle-animate');
      void btn.offsetWidth;   // force reflow
      btn.classList.add('theme-toggle-animate');
    }

    return next;
  }

  function init() {
    // Apply immediately before paint to avoid flash
    applyTheme(getCurrentTheme());

    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!getSavedTheme()) applyTheme(e.matches ? DARK : LIGHT);
    });

    // Bind all toggle buttons (in topbar AND any inline toggles)
    document.addEventListener('click', e => {
      if (e.target.closest('.theme-toggle')) toggleTheme();
    });

    // Keyboard shortcut: Ctrl/Cmd + Shift + L
    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'L') {
        e.preventDefault();
        toggleTheme();
      }
    });
  }

  return { init, toggle: toggleTheme, current: getCurrentTheme };
})();

// Run immediately — before DOM fully loads
ThemeManager.init();
