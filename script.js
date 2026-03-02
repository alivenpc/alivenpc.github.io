document.addEventListener('DOMContentLoaded', () => {
    
    const header = document.querySelector('.site-header');

    const updateScrollOffset = () => {
        const headerHeight = header ? Math.ceil(header.getBoundingClientRect().height) : 0;
        const scrollOffset = headerHeight + 8;
        document.documentElement.style.setProperty('--scroll-offset', `${scrollOffset}px`);
    };

    updateScrollOffset();
    window.addEventListener('resize', updateScrollOffset);
    window.addEventListener('load', updateScrollOffset);

    // Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
                targetElement.scrollIntoView({
                    behavior: prefersReducedMotion ? 'auto' : 'smooth',
                    block: 'start'
                });

                const adjustDelay = prefersReducedMotion ? 0 : 350;
                setTimeout(() => {
                    const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
                    const targetTop = targetElement.getBoundingClientRect().top;
                    const delta = targetTop - headerBottom;
                    if (Math.abs(delta) > 1) {
                        window.scrollBy({ top: delta, behavior: 'auto' });
                    }
                }, adjustDelay);
            }
        });
    });

    // Intersection Observer for Fade-in Animations
    const observerOptions = {
        root: null, // viewport
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of element is visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing once visible to run animation only once
                observer.unobserve(entry.target); 
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in-up, .card, .timeline-item, .vision-content');
    fadeElements.forEach(el => {
        // Ensure initial state is set for elements that might have missed the class in HTML
        el.classList.add('fade-in-up'); 
        observer.observe(el);
    });

    // Active Navigation Highlight on Scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.main-nav a');

    // Initial call to set active link
    window.addEventListener('scroll', () => {
        let current = '';
        
        // Check if we've reached the bottom of the page
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 10) {
             const lastSection = sections[sections.length - 1];
             if (lastSection) {
                 current = lastSection.getAttribute('id');
             }
        } else {
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                // const sectionHeight = section.clientHeight; // Unused
                // -150 offset to handle header and early trigger
                if (pageYOffset >= (sectionTop - 150)) {
                    current = section.getAttribute('id');
                }
            });
        }

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });

        // Header Logo Visibility Control
        const header = document.querySelector('.site-header');
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // --- Theme Switcher ---
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    // const headerLogo = document.getElementById('header-logo'); // Header logo removed
    const titleLogo = document.getElementById('title-logo');

    function updateLogos(theme) {
        // Theme format: 'dark-theme' or 'light-theme'
        const mode = theme.includes('light') ? 'light' : 'dark';
        // if (headerLogo) headerLogo.src = `assets/logo/${mode}/logo_header.png`;
        if (titleLogo) titleLogo.src = `assets/logo/${mode}/logo_title.png`;
    }

    // Check for saved user preference, if any, on load of the website
    const savedTheme = localStorage.getItem('theme');
    let currentTheme = 'dark-theme'; // Default fallback

    if (savedTheme) {
        body.className = savedTheme;
        currentTheme = savedTheme;
    } else {
        // Time-based default theme logic
        // 9:00 AM to 9:00 PM (21:00) -> Light Theme
        // 9:00 PM to 9:00 AM -> Dark Theme
        const currentHour = new Date().getHours();
        const isDayTime = currentHour >= 9 && currentHour < 21;
        
        if (isDayTime) {
            currentTheme = 'light-theme';
        } else {
            currentTheme = 'dark-theme';
        }
        
        // Apply the determined theme
        body.classList.remove('dark-theme', 'light-theme');
        body.classList.add(currentTheme);
    }
    updateLogos(currentTheme);

    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('dark-theme')) {
            body.classList.replace('dark-theme', 'light-theme');
            localStorage.setItem('theme', 'light-theme');
            updateLogos('light-theme');
        } else {
            body.classList.replace('light-theme', 'dark-theme');
            localStorage.setItem('theme', 'dark-theme');
            updateLogos('dark-theme');
        }
    });

    // --- i18n / Language Switcher ---
    const langToggle = document.getElementById('lang-toggle');
    let currentLang = 'zh'; // Default language set to Chinese

    const translations = {
        'en': {
            'nav.home': 'Home',
            'nav.concept': 'Concept',
            'nav.progress': 'Progress',
            'nav.vision': 'Vision',
            'home.slogan': 'Building NPCs That Understand.',
            'home.subSlogan': 'From Scripted Characters to Living Intelligence.',
            'home.description': 'A modular framework for constructing cognitive, memory-driven, and conscious virtual entities.',
            'home.explore': 'Explore System',
            'intro.title': 'Core Concept',
            'intro.text1': 'AliveNPC is not just a chatbot wrapper. It is a comprehensive <strong>Understanding-type NPC System</strong> designed to give virtual characters true cognitive capabilities.',
            'intro.text2': 'Moving beyond simple state machines, AliveNPC integrates perception, memory, and consciousness modules to create characters that remember, learn, and act with intent.',
            'modules.perception': 'Perception',
            'modules.memory': 'Memory',
            'modules.consciousness': 'Consciousness',
            'modules.behavior': 'Behavior',
            'modules.narrator': 'Narrator',
            'progress.title': 'Development Progress',
            'progress.item1.title': 'Architecture Design',
            'progress.item1.desc': 'Core modular structure and data flow definitions finalized.',
            'progress.item2.title': 'Event Protocol',
            'progress.item2.desc': 'Standardized communication protocols between internal modules.',
            'progress.item3.title': 'Sandbox Testing Framework',
            'progress.item3.desc': 'Building the initial environment for module interaction testing.',
            'progress.item4.title': 'Memory Integration',
            'progress.item4.desc': 'Connecting vector database for long-term memory persistence.',
            'status.completed': 'Completed',
            'status.defined': 'Defined',
            'status.inProgress': 'In Progress',
            'status.planned': 'Planned',
            'vision.title': 'Vision & Philosophy',
            'vision.statement': 'Our long-term goal is to build a truly <strong>"Understanding-type NPC"</strong>—an entity that doesn\'t just recite lines, but comprehends its existence within the virtual world.',
            'vision.item1.title': 'Dynamic Games',
            'vision.item1.desc': 'NPCs that adapt to player choices in real-time without rigid scripting.',
            'vision.item2.title': 'Virtual Worlds',
            'vision.item2.desc': 'Autonomous agents populating the metaverse with genuine interactions.',
            'vision.item3.title': 'AI Narrative',
            'vision.item3.desc': 'Systems capable of co-creating stories with human users.'
        },
        'zh': {
            'nav.home': '首页',
            'nav.concept': '核心理念',
            'nav.progress': '开发进度',
            'nav.vision': '未来愿景',
            'home.slogan': '构建真正“理解”的 NPC',
            'home.subSlogan': '从脚本角色到鲜活智能',
            'home.description': '一个用于构建具备认知、记忆和意识的虚拟实体的模块化框架。',
            'home.explore': '探索系统',
            'intro.title': '核心理念',
            'intro.text1': 'AliveNPC 不仅仅是一个聊天机器人外壳。它是一个全面的<strong>理解型 NPC 系统</strong>，旨在赋予虚拟角色真正的认知能力。',
            'intro.text2': '超越简单的状态机，AliveNPC 集成了感知、记忆和意识模块，创造出能够记忆、学习并有意图行动的角色。',
            'modules.perception': '感知模块',
            'modules.memory': '记忆模块',
            'modules.consciousness': '意识模块',
            'modules.behavior': '行为模块',
            'modules.narrator': '叙事器',
            'progress.title': '开发进度',
            'progress.item1.title': '架构设计',
            'progress.item1.desc': '核心模块结构和数据流定义已完成。',
            'progress.item2.title': '事件协议',
            'progress.item2.desc': '内部模块之间的标准化通信协议。',
            'progress.item3.title': '沙盒测试框架',
            'progress.item3.desc': '正在构建用于模块交互测试的初始环境。',
            'progress.item4.title': '记忆集成',
            'progress.item4.desc': '连接向量数据库以实现长期记忆持久化。',
            'status.completed': '已完成',
            'status.defined': '已定义',
            'status.inProgress': '进行中',
            'status.planned': '计划中',
            'vision.title': '愿景与哲学',
            'vision.statement': '我们的长期目标是构建真正的<strong>“理解型 NPC”</strong>——一个不仅仅背诵台词，而是理解其在虚拟世界中存在的实体。',
            'vision.item1.title': '动态游戏',
            'vision.item1.desc': '无需僵化脚本即可实时适应玩家选择的 NPC。',
            'vision.item2.title': '虚拟世界',
            'vision.item2.desc': '在元宇宙中进行真实互动的自主智能体。',
            'vision.item3.title': 'AI 叙事',
            'vision.item3.desc': '能够与人类用户共同创作故事的系统。'
        }
    };

    function updateContent(lang) {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                if (element.tagName === 'STRONG' || element.innerHTML.includes('<strong')) {
                    element.innerHTML = translations[lang][key];
                } else {
                    element.textContent = translations[lang][key];
                }
            }
        });
        
        // No longer updating button text, select value updates automatically
    }

    // Initialize language
    if (langToggle) {
        langToggle.value = currentLang;
        updateContent(currentLang);
    }
    
    // langToggle.addEventListener('click', () => { // Old button logic
    langToggle.addEventListener('change', (e) => {
        currentLang = e.target.value;
        updateContent(currentLang);
    });

    // Initialize with default or user preference if we were to save it
    // updateContent('en'); 

    // --- Mobile Menu Toggle ---
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileToggle && mainNav) {
        mobileToggle.addEventListener('click', () => {
            mobileToggle.classList.toggle('active');
            mainNav.classList.toggle('active');
            // Prevent background scrolling when menu is open
            document.body.style.overflow = mainNav.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when a link is clicked
        const navLinks = mainNav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileToggle.classList.remove('active');
                mainNav.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }
});
