    document.addEventListener("DOMContentLoaded", function() {
       const slides = document.querySelectorAll(".discount");
       let currentIndex = 0;

    function showSlide(index) {
        slides.forEach((discount, i) => {
            discount.classList.remove("active");
            if (i === index) {
                discount.classList.add("active");
            }
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    // Show the first slide initially
    showSlide(currentIndex);

    // Automatically move to the next slide every 3 seconds
    setInterval(nextSlide, 3000);
});