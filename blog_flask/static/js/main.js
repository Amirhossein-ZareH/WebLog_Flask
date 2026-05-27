// GSAP انیمیشن‌های عمومی
gsap.registerPlugin(ScrollTrigger, TextPlugin);

// انیمیشن اسکرول برای المنت‌ها
document.addEventListener('DOMContentLoaded', function() {
    // انیمیشن برای کارت‌ها
    gsap.utils.toArray('.card').forEach(card => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 90%',
                toggleActions: 'play none none reverse'
            },
            duration: 0.6,
            y: 30,
            opacity: 0,
            ease: 'power2.out'
        });
    });
    
    // انیمیشن برای دکمه‌ها
    gsap.utils.toArray('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, { duration: 0.2, scale: 1.05, y: -2 });
        });
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, { duration: 0.2, scale: 1, y: 0 });
        });
    });
});

// اسکرول به بالا
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// نمایش دکمه اسکرول
window.addEventListener('scroll', function() {
    const scrollBtn = document.getElementById('scrollToTopBtn') || 
                      document.querySelector('.scroll-to-top');
    if (scrollBtn) {
        if (window.pageYOffset > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    }
});

// ایجاد اثر تایپینگ برای تایتل‌ها
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// افکت Hover برای لینک‌ها
document.querySelectorAll('a').forEach(link => {
    link.addEventListener('mouseenter', function(e) {
        gsap.to(this, { duration: 0.2, scale: 1.02 });
    });
    link.addEventListener('mouseleave', function(e) {
        gsap.to(this, { duration: 0.2, scale: 1 });
    });
});

// اعتبارسنجی فرم در همه صفحات
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
            
            gsap.fromTo(input, 
                { x: 0 },
                { x: 10, duration: 0.1, repeat: 3, yoyo: true }
            );
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// لودینگ اسکرین
window.addEventListener('load', function() {
    const loader = document.querySelector('.loading-screen');
    if (loader) {
        setTimeout(() => {
            gsap.to(loader, {
                duration: 0.5,
                opacity: 0,
                y: -20,
                onComplete: () => loader.style.display = 'none'
            });
        }, 500);
    }
});

// Dark Mode (اختیاری)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}