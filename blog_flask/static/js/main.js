// اسکرول نرم به بالا
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// نمایش دکمه اسکرول به بالا
window.addEventListener('scroll', function() {
    const scrollBtn = document.getElementById('scrollToTopBtn');
    if (scrollBtn) {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    }
});

// دکمه اسکرول به بالا در HTML اضافه کنید
document.addEventListener('DOMContentLoaded', function() {
    const scrollBtn = document.createElement('button');
    scrollBtn.id = 'scrollToTopBtn';
    scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollBtn.onclick = scrollToTop;
    document.body.appendChild(scrollBtn);
    
    // استایل دکمه
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 30px;
        background: var(--primary);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        display: none;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
        font-size: 1.2rem;
    `;
    
    scrollBtn.addEventListener('mouseover', function() {
        this.style.transform = 'scale(1.1)';
    });
    
    scrollBtn.addEventListener('mouseout', function() {
        this.style.transform = 'scale(1)';
    });
});