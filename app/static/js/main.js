/* ============================================
   VITACLINIC - SCRIPTS PRINCIPALES
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // --------------------------------------------
    // HERO CAROUSEL
    // --------------------------------------------
    const heroCarousel = {
        currentSlide: 0,
        slides: document.querySelectorAll('.hero-slide'),
        dots: document.querySelectorAll('.hero-dot'),
        autoPlayInterval: null,
        autoPlayDelay: 6000,

        init() {
            this.startAutoPlay();
            this.bindEvents();
        },

        updateSlide() {
            this.slides.forEach((slide, index) => {
                slide.classList.remove('active');
                this.dots[index].classList.remove('active');
            });
            this.slides[this.currentSlide].classList.add('active');
            this.dots[this.currentSlide].classList.add('active');
        },

        changeSlide(direction) {
            this.currentSlide = (this.currentSlide + direction + this.slides.length) % this.slides.length;
            this.updateSlide();
            this.resetAutoPlay();
        },

        goToSlide(index) {
            this.currentSlide = index;
            this.updateSlide();
            this.resetAutoPlay();
        },

        startAutoPlay() {
            this.autoPlayInterval = setInterval(() => {
                this.changeSlide(1);
            }, this.autoPlayDelay);
        },

        resetAutoPlay() {
            clearInterval(this.autoPlayInterval);
            this.startAutoPlay();
        },

        bindEvents() {
            // Dots click events
            this.dots.forEach((dot, index) => {
                dot.addEventListener('click', () => this.goToSlide(index));
            });
        }
    };

    // Initialize hero carousel
    heroCarousel.init();

    // Global functions for hero arrows (called from HTML onclick)
    window.changeHeroSlide = (direction) => heroCarousel.changeSlide(direction);
    window.goToHeroSlide = (index) => heroCarousel.goToSlide(index);


    // --------------------------------------------
    // SERVICES CAROUSEL
    // --------------------------------------------
    const servicesCarousel = {
        position: 0,
        container: document.getElementById('servicesCarousel'),
        cards: null,
        cardWidth: 380,
        visibleCards: 3,

        init() {
            if (!this.container) return;
            this.cards = this.container.querySelectorAll('.service-card');
            this.updateVisibleCards();
            window.addEventListener('resize', () => this.updateVisibleCards());
        },

        updateVisibleCards() {
            const windowWidth = window.innerWidth;
            if (windowWidth < 768) {
                this.visibleCards = 1;
                this.cardWidth = 330;
            } else if (windowWidth < 1024) {
                this.visibleCards = 2;
                this.cardWidth = 380;
            } else {
                this.visibleCards = 3;
                this.cardWidth = 380;
            }
        },

        move(direction) {
            const maxPosition = -(this.cards.length - this.visibleCards) * this.cardWidth;
            this.position += direction * this.cardWidth;
            this.position = Math.max(maxPosition, Math.min(0, this.position));
            this.container.style.transform = `translateX(${this.position}px)`;
        }
    };

    // Initialize services carousel
    servicesCarousel.init();

    // Global function for services carousel
    window.moveServicesCarousel = (direction) => servicesCarousel.move(direction);


    // --------------------------------------------
    // DOCTORS CAROUSEL
    // --------------------------------------------
    const doctorsCarousel = {
        position: 0,
        container: document.getElementById('doctorsCarousel'),
        cards: null,
        cardWidth: 350,
        visibleCards: 3,

        init() {
            if (!this.container) return;
            this.cards = this.container.querySelectorAll('.doctor-card');
            this.updateVisibleCards();
            window.addEventListener('resize', () => this.updateVisibleCards());
        },

        updateVisibleCards() {
            const windowWidth = window.innerWidth;
            if (windowWidth < 768) {
                this.visibleCards = 1;
                this.cardWidth = 330;
            } else if (windowWidth < 1024) {
                this.visibleCards = 2;
                this.cardWidth = 350;
            } else {
                this.visibleCards = 3;
                this.cardWidth = 350;
            }
        },

        move(direction) {
            const maxPosition = -(this.cards.length - this.visibleCards) * this.cardWidth;
            this.position += direction * this.cardWidth;
            this.position = Math.max(maxPosition, Math.min(0, this.position));
            this.container.style.transform = `translateX(${this.position}px)`;
        }
    };

    // Initialize doctors carousel
    doctorsCarousel.init();

    // Global function for doctors carousel
    window.moveDoctorsCarousel = (direction) => doctorsCarousel.move(direction);


    // --------------------------------------------
    // TESTIMONIALS CAROUSEL
    // --------------------------------------------
    const testimonialsCarousel = {
        currentSlide: 0,
        slides: document.querySelectorAll('.testimonial-slide'),
        dots: document.querySelectorAll('.testimonial-dot'),
        autoPlayInterval: null,
        autoPlayDelay: 5000,

        init() {
            if (this.slides.length === 0) return;
            this.startAutoPlay();
            this.bindEvents();
        },

        goToSlide(index) {
            this.slides.forEach((slide, i) => {
                slide.classList.remove('active');
                this.dots[i].classList.remove('active');
            });
            this.currentSlide = index;
            this.slides[this.currentSlide].classList.add('active');
            this.dots[this.currentSlide].classList.add('active');
            this.resetAutoPlay();
        },

        nextSlide() {
            const nextIndex = (this.currentSlide + 1) % this.slides.length;
            this.goToSlide(nextIndex);
        },

        startAutoPlay() {
            this.autoPlayInterval = setInterval(() => {
                this.nextSlide();
            }, this.autoPlayDelay);
        },

        resetAutoPlay() {
            clearInterval(this.autoPlayInterval);
            this.startAutoPlay();
        },

        bindEvents() {
            this.dots.forEach((dot, index) => {
                dot.addEventListener('click', () => this.goToSlide(index));
            });
        }
    };

    // Initialize testimonials carousel
    testimonialsCarousel.init();

    // Global function for testimonials
    window.goToTestimonial = (index) => testimonialsCarousel.goToSlide(index);


    // --------------------------------------------
    // NAVBAR SCROLL EFFECT
    // --------------------------------------------
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.top = '10px';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.85)';
                navbar.style.top = '20px';
            }
        });
    }


    // --------------------------------------------
    // SMOOTH SCROLL FOR NAV LINKS
    // --------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                target.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
        });
    });


    // --------------------------------------------
    // ACTIVE NAV LINK ON SCROLL
    // --------------------------------------------
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    function updateActiveNavLink() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 200;
            if (window.scrollY >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveNavLink);


    // --------------------------------------------
    // INTERSECTION OBSERVER FOR ANIMATIONS
    // --------------------------------------------
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    document.querySelectorAll('.service-card, .doctor-card, .stat-item').forEach(el => {
        animationObserver.observe(el);
    });


    // --------------------------------------------
    // TOUCH/SWIPE SUPPORT FOR CAROUSELS
    // --------------------------------------------
    function addSwipeSupport(container, moveCallback) {
        if (!container) return;
        
        let startX = 0;
        let startY = 0;
        let isDragging = false;

        container.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isDragging = true;
        }, { passive: true });

        container.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            
            const diffX = e.touches[0].clientX - startX;
            const diffY = e.touches[0].clientY - startY;
            
            // Check if horizontal swipe
            if (Math.abs(diffX) > Math.abs(diffY)) {
                e.preventDefault();
            }
        }, { passive: false });

        container.addEventListener('touchend', (e) => {
            if (!isDragging) return;
            
            const endX = e.changedTouches[0].clientX;
            const diffX = endX - startX;
            
            if (Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    moveCallback(-1);
                } else {
                    moveCallback(1);
                }
            }
            
            isDragging = false;
        }, { passive: true });
    }

    // Add swipe support to carousels
    addSwipeSupport(
        document.querySelector('.services-carousel-container'),
        (dir) => servicesCarousel.move(dir)
    );
    
    addSwipeSupport(
        document.querySelector('.doctors-carousel-container'),
        (dir) => doctorsCarousel.move(dir)
    );


    // --------------------------------------------
    // KEYBOARD NAVIGATION FOR ACCESSIBILITY
    // --------------------------------------------
    document.addEventListener('keydown', (e) => {
        // Only handle if not in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        
        switch(e.key) {
            case 'ArrowLeft':
                heroCarousel.changeSlide(-1);
                break;
            case 'ArrowRight':
                heroCarousel.changeSlide(1);
                break;
        }
    });


    // --------------------------------------------
    // STATS COUNTER ANIMATION
    // --------------------------------------------
    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format number
            let displayValue = Math.floor(current);
            if (target >= 1000) {
                displayValue = Math.floor(current / 1000) + 'K+';
            } else if (target === 98) {
                displayValue = Math.floor(current) + '%';
            } else {
                displayValue = Math.floor(current) + '+';
            }
            
            element.textContent = displayValue;
        }, 16);
    }

    // Observe stats section for counter animation
    const statsSection = document.querySelector('.stats-section');
    let statsAnimated = false;

    if (statsSection) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !statsAnimated) {
                    statsAnimated = true;
                    
                    const statNumbers = document.querySelectorAll('.stat-number');
                    const targets = [25000, 50, 20, 98];
                    
                    statNumbers.forEach((stat, index) => {
                        animateCounter(stat, targets[index]);
                    });
                }
            });
        }, { threshold: 0.5 });

        statsObserver.observe(statsSection);
    }

});