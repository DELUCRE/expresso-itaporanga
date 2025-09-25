// JavaScript principal da Expresso Itaporanga
// Funcionalidades de interatividade e acessibilidade

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initializeFormValidation();
    initializeMenuInteraction();
    initializeAccessibilityFeatures();
    initializeAnimations();
    initializeContactForm();
});

// Validação de formulários em tempo real
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
        
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showFormError('Por favor, corrija os erros antes de enviar.');
            }
        });
    });
}

// Validar campo individual
function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    const isRequired = field.hasAttribute('required');
    
    // Limpar erros anteriores
    clearFieldError(field);
    
    // Validar campo obrigatório
    if (isRequired && !value) {
        showFieldError(field, 'Este campo é obrigatório.');
        return false;
    }
    
    // Validações específicas por tipo
    switch (fieldType) {
        case 'email':
            if (value && !isValidEmail(value)) {
                showFieldError(field, 'Por favor, insira um email válido.');
                return false;
            }
            break;
            
        case 'tel':
            if (value && !isValidPhone(value)) {
                showFieldError(field, 'Por favor, insira um telefone válido.');
                return false;
            }
            break;
    }
    
    return true;
}

// Validar formulário completo
function validateForm(form) {
    const fields = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    fields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Mostrar erro no campo
function showFieldError(field, message) {
    field.classList.add('error');
    field.setAttribute('aria-invalid', 'true');
    
    // Remover mensagem de erro anterior
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Adicionar nova mensagem de erro
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.setAttribute('role', 'alert');
    errorDiv.setAttribute('aria-live', 'polite');
    
    field.parentNode.appendChild(errorDiv);
}

// Limpar erro do campo
function clearFieldError(field) {
    field.classList.remove('error');
    field.removeAttribute('aria-invalid');
    
    const errorMessage = field.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

// Mostrar erro geral do formulário
function showFormError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-error';
    alertDiv.textContent = message;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.setAttribute('aria-live', 'assertive');
    
    // Inserir no topo da página
    const main = document.querySelector('main');
    main.insertBefore(alertDiv, main.firstChild);
    
    // Remover após 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
    
    // Focar no primeiro campo com erro
    const firstError = document.querySelector('.error');
    if (firstError) {
        firstError.focus();
    }
}

// Validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validar telefone
function isValidPhone(phone) {
    const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
    return phoneRegex.test(phone);
}

// Interação do menu de navegação
function initializeMenuInteraction() {
    const menuItems = document.querySelectorAll('.nav-menu a');
    
    menuItems.forEach(item => {
        item.addEventListener('focus', function() {
            this.classList.add('focused');
        });
        
        item.addEventListener('blur', function() {
            this.classList.remove('focused');
        });
        
        item.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
}

// Recursos de acessibilidade
function initializeAccessibilityFeatures() {
    // Adicionar skip link
    addSkipLink();
    
    // Melhorar navegação por teclado
    improveKeyboardNavigation();
    
    // Adicionar indicadores de foco visíveis
    addFocusIndicators();
    
    // Configurar ARIA labels
    setupAriaLabels();
}

// Adicionar link para pular para conteúdo principal
function addSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Pular para o conteúdo principal';
    skipLink.className = 'skip-link';
    skipLink.setAttribute('aria-label', 'Pular navegação e ir direto para o conteúdo');
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Adicionar ID ao conteúdo principal se não existir
    const main = document.querySelector('main');
    if (main && !main.id) {
        main.id = 'main-content';
    }
}

// Melhorar navegação por teclado
function improveKeyboardNavigation() {
    // Tornar elementos interativos focáveis
    const interactiveElements = document.querySelectorAll('.feature-card, .value-card, .stat-card');
    
    interactiveElements.forEach(element => {
        if (!element.hasAttribute('tabindex')) {
            element.setAttribute('tabindex', '0');
        }
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                // Simular clique se houver link dentro do elemento
                const link = this.querySelector('a');
                if (link) {
                    link.click();
                }
            }
        });
    });
}

// Adicionar indicadores de foco visíveis
function addFocusIndicators() {
    const focusableElements = document.querySelectorAll('a, button, input, select, textarea, [tabindex]');
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('keyboard-focus');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('keyboard-focus');
        });
        
        element.addEventListener('mousedown', function() {
            this.classList.add('mouse-focus');
        });
        
        element.addEventListener('mouseup', function() {
            this.classList.remove('mouse-focus');
        });
    });
}

// Configurar ARIA labels
function setupAriaLabels() {
    // Adicionar labels aos ícones
    const icons = document.querySelectorAll('.feature-icon, .value-icon');
    icons.forEach(icon => {
        if (!icon.getAttribute('aria-label')) {
            icon.setAttribute('aria-hidden', 'true');
        }
    });
    
    // Melhorar formulários
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        const label = group.querySelector('label');
        const input = group.querySelector('input, select, textarea');
        
        if (label && input && !input.getAttribute('aria-describedby')) {
            const labelId = 'label-' + Math.random().toString(36).substr(2, 9);
            label.id = labelId;
            input.setAttribute('aria-labelledby', labelId);
        }
    });
}

// Animações suaves
function initializeAnimations() {
    // Animação de entrada para elementos
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animatedElements = document.querySelectorAll('.feature-card, .value-card, .section-title');
    animatedElements.forEach(element => {
        element.classList.add('animate-ready');
        observer.observe(element);
    });
}

// Funcionalidades específicas do formulário de contato
function initializeContactForm() {
    const contactForm = document.querySelector('#contact-form');
    if (!contactForm) return;
    
    // Máscara para telefone
    const phoneInput = contactForm.querySelector('input[type="tel"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            this.value = formatPhone(this.value);
        });
    }
    
    // Envio AJAX do formulário
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm(this)) {
            submitContactForm(this);
        }
    });
}

// Formatar telefone
function formatPhone(phone) {
    // Remove tudo que não é dígito
    phone = phone.replace(/\D/g, '');
    
    // Aplica a máscara
    if (phone.length <= 10) {
        phone = phone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else {
        phone = phone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    }
    
    return phone;
}

// Enviar formulário de contato via AJAX
function submitContactForm(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Desabilitar botão durante envio
    submitButton.disabled = true;
    submitButton.textContent = 'Enviando...';
    
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessMessage('Mensagem enviada com sucesso! Entraremos em contato em breve.');
            form.reset();
        } else {
            showFormError(data.message || 'Erro ao enviar mensagem. Tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showFormError('Erro ao enviar mensagem. Verifique sua conexão e tente novamente.');
    })
    .finally(() => {
        // Reabilitar botão
        submitButton.disabled = false;
        submitButton.textContent = 'Enviar Mensagem';
    });
}

// Mostrar mensagem de sucesso
function showSuccessMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success';
    alertDiv.textContent = message;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.setAttribute('aria-live', 'polite');
    
    const main = document.querySelector('main');
    main.insertBefore(alertDiv, main.firstChild);
    
    // Remover após 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
    
    // Scroll para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
