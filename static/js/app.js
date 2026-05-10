// Traveloop App JS - Premium UI Interactions

// Apply Chart.js theme based on current data-bs-theme
function applyChartTheme() {
  const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
  if (!window.Chart) return;

  const textColor = isDark ? '#A8A29E' : '#57534E';
  const gridColor = isDark ? '#2C2420' : '#E7E5E4';
  const bgColor   = isDark ? '#1E1A17' : '#FFFFFF';

  Chart.defaults.color            = textColor;
  Chart.defaults.borderColor      = gridColor;
  Chart.defaults.backgroundColor  = bgColor;

  if (Chart.defaults.plugins.legend) {
    Chart.defaults.plugins.legend.labels.color = textColor;
  }
}

// Re-apply when theme changes (observe attribute change)
const themeObserver = new MutationObserver(() => applyChartTheme());
themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-bs-theme'] });

document.addEventListener('DOMContentLoaded', applyChartTheme);

// Consistent palette for both modes
const CHART_COLORS = {
  gold:    '#F59E0B',
  teal:    '#0D9488',
  indigo:  '#6366F1',
  rose:    '#F43F5E',
  sky:     '#0EA5E9',
  lime:    '#84CC16',
};

// Semi-transparent fills
const CHART_BG = Object.fromEntries(
  Object.entries(CHART_COLORS).map(([k, v]) => [k, v + '33'])
);

document.addEventListener('DOMContentLoaded', () => {
    // 1. Starfield animation for dashboard hero
    initStarfield('starfield');

    // 2. Number counter animation for stat cards
    document.querySelectorAll('[data-counter]').forEach(el => {
        animateCounter(el, parseInt(el.dataset.counter, 10));
    });

    // 3. Scroll reveal for cards
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity = 1;
                e.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.card, .slide-up').forEach(el => {
        // Only apply if not already handled by Alpine or specific inline styles
        if (!el.style.animationDelay) {
            el.style.opacity = 0;
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s cubic-bezier(0.22, 1, 0.36, 1), transform 0.6s cubic-bezier(0.22, 1, 0.36, 1)';
            observer.observe(el);
        }
    });

    // 4. Budget progress bar animated fill on page load
    document.querySelectorAll('[data-progress]').forEach(bar => {
        const value = bar.dataset.progress;
        setTimeout(() => bar.style.width = value + '%', 300);
    });

    // 5. AJAX form handlers for checklist toggles
    document.querySelectorAll('.toggle-packed').forEach(cb => {
        cb.addEventListener('change', async function() {
            try {
                const res = await fetch(`/packing/${this.dataset.id}/toggle/`, {
                    method: 'POST',
                    headers: { 
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json'
                    }
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    const textSpan = document.getElementById(`packing-text-${this.dataset.id}`);
                    if (data.is_packed) {
                        textSpan.style.textDecoration = 'line-through';
                        textSpan.style.opacity = '0.5';
                    } else {
                        textSpan.style.textDecoration = 'none';
                        textSpan.style.opacity = '1';
                    }
                }
            } catch (err) {
                console.error("Failed to toggle packing item", err);
            }
        });
    });
});

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value
        || document.cookie.match(/csrftoken=([^;]+)/)?.[1];
}

function initStarfield(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let stars = [];

    function resize() {
        width = canvas.width = canvas.offsetWidth;
        height = canvas.height = canvas.offsetHeight;
        initStars();
    }

    function initStars() {
        stars = [];
        const numStars = Math.floor((width * height) / 3000); // Density
        for (let i = 0; i < numStars; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5,
                vx: Math.random() * 0.2 - 0.1,
                vy: Math.random() * 0.2 - 0.1,
                alpha: Math.random(),
                dAlpha: Math.random() * 0.02 - 0.01
            });
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        stars.forEach(star => {
            // Move
            star.x += star.vx;
            star.y += star.vy;
            
            // Wrap
            if (star.x < 0) star.x = width;
            if (star.x > width) star.x = 0;
            if (star.y < 0) star.y = height;
            if (star.y > height) star.y = 0;
            
            // Twinkle
            star.alpha += star.dAlpha;
            if (star.alpha <= 0.1 || star.alpha >= 1) star.dAlpha *= -1;
            
            // Draw
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(240, 237, 230, ${star.alpha})`; // text-primary color
            ctx.fill();
        });
        
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', resize);
    resize();
    animate();
}

function animateCounter(el, target, duration = 1200) {
    let start = null;
    const initial = parseInt(el.innerText || '0', 10);
    
    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        
        // Easing function: easeOutQuart
        const easeProgress = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(initial + (target - initial) * easeProgress);
        
        el.innerText = current;
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            el.innerText = target;
        }
    }
    window.requestAnimationFrame(step);
}

// Utility functions for forms (similar to before, updated for new styling if needed)
async function postForm(url, formData) {
    const resp = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
    return resp.json();
}

async function postJSON(url, data={}) {
    const resp = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    });
    return resp.json();
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Alpine or custom toast handles notification natively, but we can trigger a manual one if needed
        alert("Copied to clipboard!");
    });
}
