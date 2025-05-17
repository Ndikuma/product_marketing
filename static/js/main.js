// Enhanced Mobile Menu Toggle
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const menuIconOpen = document.getElementById('menu-icon-open');
const menuIconClose = document.getElementById('menu-icon-close');
const menuLinks = mobileMenu.querySelectorAll('a');

function toggleMenu() {
    const isExpanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true';
    mobileMenuToggle.setAttribute('aria-expanded', !isExpanded);
    mobileMenu.classList.toggle('hidden');
    menuIconOpen.classList.toggle('hidden');
    menuIconClose.classList.toggle('hidden');
    document.body.style.overflow = isExpanded ? 'auto' : 'hidden';

    // Focus management
    if (!isExpanded) {
        mobileMenu.querySelector('a').focus();
    } else {
        mobileMenuToggle.focus();
    }
}

mobileMenuToggle.addEventListener('click', toggleMenu);

// Close menu when clicking a link
menuLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (!mobileMenu.classList.contains('hidden')) {
            toggleMenu();
        }
    });
});

// Close menu on outside click
document.addEventListener('click', (e) => {
    if (!mobileMenu.contains(e.target) && e.target !== mobileMenuToggle && !mobileMenu.classList.contains('hidden')) {
        toggleMenu();
    }
});

// Close menu on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
        toggleMenu();
    }
});

// Trap focus within mobile menu
mobileMenu.addEventListener('keydown', (e) => {
    if (e.key === 'Tab' && !mobileMenu.classList.contains('hidden')) {
        const focusableElements = mobileMenu.querySelectorAll('a, button');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
});

// Social Media Button Sheet Toggle
const socialSheetToggle = document.getElementById('social-sheet-toggle');
const socialSheet = document.getElementById('social-sheet');
const socialLinks = socialSheet.querySelectorAll('a');

function toggleSocialSheet() {
    const isExpanded = socialSheetToggle.getAttribute('aria-expanded') === 'true';
    socialSheetToggle.setAttribute('aria-expanded', !isExpanded);
    socialSheet.classList.toggle('hidden');
    socialSheet.classList.toggle('opacity-0');
    socialSheet.classList.toggle('translate-y-2');

    // Focus management
    if (!isExpanded) {
        socialSheet.querySelector('a').focus();
    } else {
        socialSheetToggle.focus();
    }
}

socialSheetToggle.addEventListener('click', toggleSocialSheet);

// Close sheet when clicking a link
socialLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (!socialSheet.classList.contains('hidden')) {
            toggleSocialSheet();
        }
    });
});

// Close sheet on outside click
document.addEventListener('click', (e) => {
    if (!socialSheet.contains(e.target) && e.target !== socialSheetToggle && !socialSheet.classList.contains('hidden')) {
        toggleSocialSheet();
    }
});

// Close sheet on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !socialSheet.classList.contains('hidden')) {
        toggleSocialSheet();
    }
});

// Trap focus within social sheet
socialSheet.addEventListener('keydown', (e) => {
    if (e.key === 'Tab' && !socialSheet.classList.contains('hidden')) {
        const focusableElements = socialSheet.querySelectorAll('a');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
});