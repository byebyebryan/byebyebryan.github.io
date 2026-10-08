(() => {
  const videos = [...document.querySelectorAll('.project-video')];
  const button = document.querySelector('.motion-toggle');
  if (!videos.length || !button || !('IntersectionObserver' in window)) return;

  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = preference.matches;
  const visible = new Set();
  const manuallyPaused = new Set();

  function sync() {
    for (const video of videos) {
      if (paused || document.hidden || !visible.has(video)) {
        video.pause();
      } else if (!manuallyPaused.has(video)) {
        video.play().catch(() => {});
      }
    }
    button.textContent = paused ? 'Play motion' : 'Pause motion';
  }

  button.hidden = false;
  button.addEventListener('click', () => {
    paused = !paused;
    if (!paused) manuallyPaused.clear();
    sync();
  });
  preference.addEventListener('change', () => {
    paused = preference.matches;
    sync();
  });
  document.addEventListener('visibilitychange', sync);

  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting && entry.intersectionRatio >= 0.15) visible.add(entry.target);
      else visible.delete(entry.target);
    }
    sync();
  }, { threshold: 0.15 });
  videos.forEach(video => {
    video.addEventListener('pause', () => {
      if (!paused && !document.hidden && visible.has(video)) manuallyPaused.add(video);
    });
    video.addEventListener('play', () => manuallyPaused.delete(video));
    observer.observe(video);
  });
  sync();
})();
