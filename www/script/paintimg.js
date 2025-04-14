document.addEventListener('DOMContentLoaded', function () {
 const images = document.querySelectorAll('img.art-image');
 const checkVisibility = () => {
  images.forEach(image => {
   const rect = image.getBoundingClientRect();
   const imageCenter = rect.top + rect.height / 2;
   const windowHeight = window.innerHeight;

   if (imageCenter < windowHeight * 0.85 && imageCenter > windowHeight * 0.15) {
    image.classList.add('visible');
   } else {
    image.classList.remove('visible');
   }
  });
 };

 checkVisibility();
 document.addEventListener('scroll', () => {
  requestAnimationFrame(checkVisibility);
 });
});
