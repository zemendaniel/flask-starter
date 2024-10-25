function copyLink(url) {
    navigator.clipboard.writeText(url).then(function() {
        createFlashMessage("Link kimásolva!", 'success')
    }, function(err) {
        createFlashMessage('Hiba történt a link másolása közben!', 'error');
    });
}
function togglePasswordVisibility(id, element) {
    const passwordField = document.getElementById(id);
    const isPasswordVisible = passwordField.type === 'text';
    passwordField.type = isPasswordVisible ? 'password' : 'text';

    const icon = element.querySelector('i');
    icon.className = isPasswordVisible ? 'fa fa-eye' : 'fa fa-eye-slash';
}

window.onscroll = function() {
    let scrollTop = window.scrollY || document.documentElement.scrollTop;
    const btn = document.getElementById('scrollToTopButton');
    if (!btn) {return;}

    if (scrollTop === 0) {
        // User is at the top
        btn.style.display = "none";
    } else if (scrollTop < lastScrollTop) {
        // User is scrolling up
        btn.style.display = "block";
    } else {
        // User is scrolling down
        btn.style.display = "none";
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
};

function backToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const entries = params.entries();
    const paramsObject = {};
    for(const [key, value] of entries) {
        paramsObject[key] = value;
    }
    return paramsObject;
}

// Function to populate form fields based on URL parameters
function populateForm(params) {
    for(const key in params) {
        const input = document.querySelector(`#${key}`);
        if(input) {
            if(input.type === 'checkbox') {
                // For checkboxes, set the checked property
                input.checked = (params[key].toLowerCase() === 'on');
            } else {
                // For other input types, set the value property
                input.value = params[key];
            }
        }
    }
}

// Get URL parameters and populate the form
document.addEventListener('DOMContentLoaded', (event) => {
    const params = getUrlParams();
    populateForm(params);
    lastScrollTop = window.scrollY || document.documentElement.scrollTop;
    amount = 0;
});

function hideSearchForm(form_id, button_id){
    document.getElementById(form_id).style.display = "none";
    document.getElementById(button_id).style.display = "block";
    localStorage.setItem(form_id, 'none');
}

function showSearchForm(form_id, button_id){
    document.getElementById(form_id).style.display = "block";
    document.getElementById(button_id).style.display = "none";
    localStorage.setItem(form_id, 'block');
}

function showOrHideFormOnLoad(form_id, button_id){
    if (window.location.search){
        document.getElementById(form_id).style.display = "block";
        document.getElementById(button_id).style.display = "none";
        return;
    }

    let form_mode = localStorage.getItem(form_id) || "none";
    let button_mode = form_mode === "none" ? "block" : "none";

    document.getElementById(form_id).style.display = form_mode;
    document.getElementById(button_id).style.display = button_mode;
}

document.body.addEventListener('htmx:configRequest', function(event) {
    document.getElementById('loading').style.display = 'flex';
});

document.body.addEventListener('htmx:afterRequest', function(event) {
    document.getElementById('loading').style.display = 'none';
    const xhr = event.detail.xhr;
    const responseHeaders = xhr.getAllResponseHeaders();
    const headersArray = responseHeaders.trim().split(/[\r\n]+/);
    headersArray.forEach(header => {
        const [key, value] = header.split(': ');
        if (key === 'x-amount') {
            amount = value;
        }
    });
    const amount_element = document.getElementById('amount');
    if (amount_element){
        amount_element.textContent = amount + " találat";
    }
});

document.body.addEventListener('htmx:responseError', function(event) {
    document.getElementById('loading').style.display = 'none';
});
