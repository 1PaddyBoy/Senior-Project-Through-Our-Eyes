function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

// Fade-in animation trigger
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("nav ul li a").forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const sectionId = this.getAttribute("href").substring(1);
            document.getElementById(sectionId).scrollIntoView({ behavior: "smooth" });
        });
    });
});

document.addEventListener("scroll", () => {
    const scrollPos = window.scrollY;
    document.querySelector(".layer1").style.transform = `translateY(${-scrollPos * 0.2}px)`;
    document.querySelector(".layer2").style.transform = `translateY(${scrollPos * 0.1}px)`;
});