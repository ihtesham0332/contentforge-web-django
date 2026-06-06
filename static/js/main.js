document.addEventListener('DOMContentLoaded', function() {

  // --- Fade-in-up on scroll (Intersection Observer) ---
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-in-up').forEach(el => observer.observe(el));

  // --- Tab system ---
  document.querySelectorAll('[data-tab-group]').forEach(group => {
    const tabs = group.querySelectorAll('[data-tab]');
    const panes = group.querySelectorAll('[data-pane]');
    tabs.forEach(tab => {
      tab.addEventListener('click', function(e) {
        e.preventDefault();
        const target = this.dataset.tab;
        tabs.forEach(t => t.classList.remove('active'));
        panes.forEach(p => p.classList.remove('active'));
        this.classList.add('active');
        const pane = group.querySelector(`[data-pane="${target}"]`);
        if (pane) pane.classList.add('active');
      });
    });
  });

  // --- Copy to clipboard with toast ---
  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', function() {
      const target = document.querySelector(this.dataset.copy);
      if (!target) return;
      const text = target.innerText || target.textContent;
      navigator.clipboard.writeText(text.trim()).then(() => showToast('Copied to clipboard!', 'success'));
    });
  });

  // --- Toast system ---
  window.showToast = function(message, type) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    const colors = { success: 'bg-emerald-500', error: 'bg-rose-500', info: 'bg-indigo-500', warning: 'bg-amber-500' };
    toast.className = `toast-slide ${colors[type] || colors.info} text-white px-5 py-3 rounded-xl shadow-lg text-sm font-medium flex items-center gap-2`;
    const icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };
    toast.innerHTML = `<span class="text-lg font-bold">${icons[type] || icons.info}</span> ${message}`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.3s'; setTimeout(() => toast.remove(), 300); }, 2500);
  };

  // --- Button loading state ---
  document.querySelectorAll('[data-loading]').forEach(form => {
    form.addEventListener('submit', function() {
      const btn = this.querySelector('[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<svg class="animate-spin -ml-1 mr-2 h-4 w-4 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Processing...';
      }
    });
  });
});
