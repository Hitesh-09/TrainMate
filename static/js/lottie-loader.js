// Lottie animation loader
document.addEventListener('DOMContentLoaded', function() {
  const animationContainer = document.getElementById('lottie-loading');
  if (!animationContainer) return;
  
  const animation = lottie.loadAnimation({
    container: animationContainer,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '/static/animations/train-loading.json'
  });
});