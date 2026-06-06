document.addEventListener('DOMContentLoaded', function() {

  // --- Live character/word/sentence counter ---
  const textarea = document.getElementById('grammarTextarea');
  const charCount = document.getElementById('charCount');
  const wordCount = document.getElementById('wordCount');
  const sentenceCount = document.getElementById('sentenceCount');
  const progressBar = document.getElementById('charProgress');

  if (textarea && charCount) {
    const max = 5000;
    function updateCounts() {
      const val = textarea.value;
      const chars = val.length;
      const words = val.trim() ? val.trim().split(/\s+/).length : 0;
      const sentences = val ? (val.match(/[.!?]+/g) || []).length : 0;
      charCount.textContent = chars;
      wordCount.textContent = words;
      sentenceCount.textContent = sentences;
      if (progressBar) {
        const pct = Math.min((chars / max) * 100, 100);
        progressBar.style.width = pct + '%';
        progressBar.className = 'h-1.5 rounded-full transition-all duration-300 ' +
          (pct > 90 ? 'bg-rose-500' : pct > 75 ? 'bg-amber-500' : 'bg-emerald-500');
      }
    }
    textarea.addEventListener('input', updateCounts);
    updateCounts();
  }

  // --- Score ring animation ---
  const ring = document.getElementById('scoreRing');
  if (ring) {
    const score = parseInt(ring.dataset.score, 10);
    const circumference = 2 * Math.PI * 54;
    const offset = circumference - (score / 100) * circumference;
    const fg = ring.querySelector('.fg');
    if (fg) {
      setTimeout(() => {
        fg.style.strokeDashoffset = offset;
      }, 300);
    }
  }

  // --- Mini bar animations ---
  document.querySelectorAll('.mini-bar').forEach(bar => {
    const fill = bar.querySelector('.fill');
    if (fill) {
      setTimeout(() => {
        fill.style.width = fill.dataset.width || '0%';
      }, 400);
    }
  });

  // --- Diff view toggle ---
  const origBtn = document.getElementById('showOriginal');
  const corrBtn = document.getElementById('showCorrected');
  const origPane = document.getElementById('originalPane');
  const corrPane = document.getElementById('correctedPane');
  if (origBtn && corrBtn && origPane && corrPane) {
    origBtn.addEventListener('click', function() {
      origBtn.classList.add('bg-indigo-100', 'text-indigo-700', 'border-indigo-300');
      origBtn.classList.remove('bg-gray-100', 'text-gray-500', 'border-gray-200');
      corrBtn.classList.remove('bg-indigo-100', 'text-indigo-700', 'border-indigo-300');
      corrBtn.classList.add('bg-gray-100', 'text-gray-500', 'border-gray-200');
      origPane.classList.remove('hidden');
      corrPane.classList.add('hidden');
    });
    corrBtn.addEventListener('click', function() {
      corrBtn.classList.add('bg-indigo-100', 'text-indigo-700', 'border-indigo-300');
      corrBtn.classList.remove('bg-gray-100', 'text-gray-500', 'border-gray-200');
      origBtn.classList.remove('bg-indigo-100', 'text-indigo-700', 'border-indigo-300');
      origBtn.classList.add('bg-gray-100', 'text-gray-500', 'border-gray-200');
      corrPane.classList.remove('hidden');
      origPane.classList.add('hidden');
    });
  }
});
