// Main script for Crop Sathi Frontend

document.addEventListener('DOMContentLoaded', () => {
    // --- Constants ---
    const TOKEN_KEY = 'cropSathiAuthToken';

    // --- Element Selectors ---
    const getEl = (id) => document.getElementById(id);
    const queryEl = (selector) => document.querySelector(selector);
    const queryAll = (selector) => document.querySelectorAll(selector);

    // --- App State ---
    const state = {
        isLoggedIn: false,
        user: null, // e.g., { phone: '+91...' }
        currentAdvisory: null,
        map: null,
        mapMarker: null,
        appConfig: null, // To store crop/soil data from the backend
    };

    // --- UI Component Selectors ---
    const navbar = getEl('navbar');
    const mobileMenuButton = getEl('mobile-menu-button');
    const mobileMenu = getEl('mobile-menu');
    const advisorySection = getEl('advisory');
    const dashboardSection = getEl('dashboard');
    const loginPrompt = getEl('login-prompt');
    const advisoryFormContainer = getEl('advisory-form-container');
    const advisoryForm = getEl('advisory-form');
    const authButtons = getEl('auth-buttons');
    const userMenu = getEl('user-menu');
    const userIdentifier = getEl('user-identifier');
    const navLinks = queryAll('.nav-link');
    const fade_in_sections = queryAll('.fade-in-section');

    // Modals
    const authModalBackdrop = getEl('auth-modal-backdrop');
    const loginModal = getEl('login-modal');
    const registerModal = getEl('register-modal');
    const forgotPasswordModal = getEl('forgot-password-modal');
    const resetPasswordModal = getEl('reset-password-modal');
    const historyModalBackdrop = getEl('history-modal-backdrop');

    // --- Translations (Example) ---
    const translations = {
        en: {
            // Add keys from data-translate-key attributes here
            nav_home: "Home",
            nav_advisory: "Advisory",
            nav_dashboard: "Dashboard",
            nav_impact: "Impact",
            nav_contact: "Contact",
        },
        hi: {
            nav_home: "होम",
            nav_advisory: "सलाह",
            nav_dashboard: "डैशबोर्ड",
            nav_impact: "प्रभाव",
            nav_contact: "संपर्क",
        },
        te: {
            nav_home: "హోమ్",
            nav_advisory: "సలహా",
            nav_dashboard: "డాష్‌బోర్డ్",
            nav_impact: "ప్రభావం",
            nav_contact: "సంప్రదించండి",
        }
    };

    // ===================================================================
    // INITIALIZATION
    // ===================================================================

    function init() {
        checkForSession();
        setupEventListeners();
        initAdvisoryForm();
        initIntersectionObserver();
        checkForPasswordResetToken();
    }

    // ===================================================================
    // EVENT LISTENERS
    // ===================================================================

    function setupEventListeners() {
        // --- Navbar & Mobile Menu ---
        window.addEventListener('scroll', handleScroll);
        mobileMenuButton.addEventListener('click', toggleMobileMenu);

        // --- Auth Buttons & Modals ---
        getEl('login-btn').addEventListener('click', () => showModal(loginModal));
        getEl('register-btn').addEventListener('click', () => showModal(registerModal));
        getEl('logout-btn').addEventListener('click', handleLogout);
        
        getEl('login-prompt-link').addEventListener('click', (e) => { e.preventDefault(); showModal(loginModal); });
        getEl('register-prompt-link').addEventListener('click', (e) => { e.preventDefault(); showModal(registerModal); });

        getEl('show-register-link').addEventListener('click', (e) => { e.preventDefault(); showModal(registerModal, loginModal); });
        getEl('show-login-link').addEventListener('click', (e) => { e.preventDefault(); showModal(loginModal, registerModal); });
        
        getEl('forgot-password-link').addEventListener('click', (e) => { e.preventDefault(); showModal(forgotPasswordModal, loginModal); });
        getEl('close-forgot-modal-btn').addEventListener('click', hideAllAuthModals);
        getEl('close-reset-modal-btn').addEventListener('click', hideAllAuthModals);

        authModalBackdrop.addEventListener('click', (e) => { if (e.target === authModalBackdrop) hideAllAuthModals(); });
        queryAll('.close-modal-btn').forEach(btn => {
            btn.addEventListener('click', hideAllAuthModals);
        });

        // --- Forms ---
        advisoryForm.addEventListener('submit', handleAdvisoryFormSubmit);
        getEl('login-form').addEventListener('submit', handleLoginSubmit);
        getEl('register-form').addEventListener('submit', handleRegisterSubmit);
        getEl('forgot-password-form').addEventListener('submit', handleForgotPasswordSubmit);
        getEl('reset-password-form').addEventListener('submit', handleResetPasswordSubmit);
        getEl('clear-form-btn').addEventListener('click', clearAdvisoryForm);
        getEl('gps-button').addEventListener('click', handleGpsButtonClick);
        getEl('cropType').addEventListener('change', handleCropTypeChange);
        getEl('cropStage').addEventListener('input', handleCropStageChange);

        // --- Language ---
        getEl('language-toggle').addEventListener('change', (e) => setLanguage(e.target.value));

        // --- History ---
        getEl('history-btn').addEventListener('click', showHistoryModal);
        getEl('close-history-modal-btn').addEventListener('click', () => historyModalBackdrop.classList.add('hidden'));
        historyModalBackdrop.addEventListener('click', (e) => { if (e.target === historyModalBackdrop) historyModalBackdrop.classList.add('hidden'); });
    }

    // ===================================================================
    // UI & INTERACTIONS
    // ===================================================================

    function handleScroll() {
        // Navbar style change on scroll
        if (window.scrollY > 50) {
            navbar.classList.add('bg-white', 'shadow-lg');
            navbar.classList.remove('bg-white/80');
        } else {
            navbar.classList.remove('bg-white', 'shadow-lg');
            navbar.classList.add('bg-white/80');
        }

        // Scroll-spy for nav links
        let currentSection = '';
        queryAll('section[id]').forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - 100) {
                currentSection = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }

    function toggleMobileMenu() {
        mobileMenu.classList.toggle('hidden');
    }

    function initIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                }
            });
        }, { threshold: 0.1 });

        fade_in_sections.forEach(section => {
            observer.observe(section);
        });
    }

    function showModal(modalToShow, modalToHide = null) {
        authModalBackdrop.classList.remove('hidden');
        if (modalToHide) modalToHide.classList.add('hidden');
        modalToShow.classList.remove('hidden');
    }

    function hideAllAuthModals() {
        authModalBackdrop.classList.add('hidden');
        loginModal.classList.add('hidden');
        registerModal.classList.add('hidden');
        getEl('forgot-password-modal').classList.add('hidden');
        getEl('reset-password-modal').classList.add('hidden');
    }

    function showAppError(message, duration = 5000) {
        const errorDiv = getEl('app-error');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        setTimeout(() => errorDiv.classList.add('hidden'), duration);
    }

    function showAuthMessage(modalId, message, isError = false) {
        const messageEl = getEl(`${modalId}-message`);
        if (!messageEl) return;

        messageEl.querySelector('span').textContent = message;
        messageEl.classList.remove('hidden', 'bg-red-100', 'border-red-400', 'text-red-700', 'bg-green-100', 'border-green-400', 'text-green-700');

        if (isError) {
            messageEl.classList.add('bg-red-100', 'border-red-400', 'text-red-700');
            messageEl.querySelector('strong').textContent = 'Error!';
        } else {
            messageEl.classList.add('bg-green-100', 'border-green-400', 'text-green-700');
            messageEl.querySelector('strong').textContent = 'Success!';
        }
        setTimeout(() => messageEl.classList.add('hidden'), 5000);
    }

    // ===================================================================
    // AUTHENTICATION
    // ===================================================================

    function updateAuthStateUI() {
        if (state.isLoggedIn) {
            authButtons.classList.add('hidden');
            userMenu.classList.remove('hidden');
            userIdentifier.textContent = state.user.phone_number;
            loginPrompt.classList.add('hidden');
            advisoryFormContainer.classList.remove('hidden');
            getEl('farmerName').value = state.user.name || '';
            getEl('phoneNumber').value = state.user.phone_number || '';
            getEl('notification-prefs').classList.remove('hidden');
        } else {
            authButtons.classList.remove('hidden');
            userMenu.classList.add('hidden');
            loginPrompt.classList.remove('hidden');
            advisoryFormContainer.classList.add('hidden');
            getEl('notification-prefs').classList.add('hidden');
            getEl('farmerName').value = '';
            getEl('phoneNumber').value = '';
        }
    }

    async function checkForSession() {
        const token = localStorage.getItem(TOKEN_KEY);
        if (token) {
            await fetchCurrentUser(token);
        }
        updateAuthStateUI();
    }

    async function fetchCurrentUser(token) {
        try {
            const user = await apiFetch('/users/me/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            state.isLoggedIn = true;
            state.user = user;
            localStorage.setItem(TOKEN_KEY, token);
        } catch (error) {
            console.error("Session check failed:", error);
            handleLogout(); // Token is invalid or expired
        }
    }

    async function handleLoginSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new URLSearchParams();
        formData.append('username', form.phone.value); // Backend expects 'username'
        formData.append('password', form.password.value);

        try {
            const response = await fetch('/token', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            await fetchCurrentUser(data.access_token);
            showAuthMessage('login', 'Login successful!');
            hideAllAuthModals();
            updateAuthStateUI();

        } catch (error) {
            showAuthMessage('login', error.message, true);
        }
    }

    async function handleAutoLogin(phone, password) {
        const formData = new URLSearchParams();
        formData.append('username', phone);
        formData.append('password', password);

        try {
            const response = await fetch('/token', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Auto-login failed');
            }

            return data.access_token;
        } catch (error) {
            throw error; // Re-throw to be caught by the calling function
        }
    }

    async function handleRegisterSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const payload = {
            name: form.name.value,
            phone_number: form.phone.value,
            password: form.password.value,
        };

        try {
            const user = await apiFetch('/users/', {
                method: 'POST',
                body: JSON.stringify(payload)
            }, false); // Don't need auth for registration

            // Automatically log the user in
            const token = await handleAutoLogin(payload.phone_number, payload.password);

            // Set state directly with user data from registration and new token
            state.isLoggedIn = true;
            state.user = user;
            localStorage.setItem(TOKEN_KEY, token);

            hideAllAuthModals();
            updateAuthStateUI();

        } catch (error) {
            showAuthMessage('register', error.message, true);
        }
    }

    async function handleForgotPasswordSubmit(e) {
        e.preventDefault();
        const phone = getEl('forgot-phone').value;
        try {
            const data = await apiFetch(`/password-recovery/${phone}`, { method: 'POST' }, false);
            showAuthMessage('forgot', data.msg);
        } catch (error) {
            showAuthMessage('forgot', error.message, true);
        }
    }

    async function handleResetPasswordSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const payload = {
            token: form.querySelector('#reset-token-input').value,
            new_password: form.querySelector('#reset-password-input').value,
        };

        try {
            const data = await apiFetch('/reset-password/', {
                method: 'POST',
                body: JSON.stringify(payload)
            }, false); // No auth token needed for this endpoint

            showAuthMessage('reset', data.msg);
            // After successful reset, hide this modal and show the login modal
            setTimeout(() => showModal(loginModal, resetPasswordModal), 2000);
        } catch (error) {
            showAuthMessage('reset', error.message, true);
        }
    }

    function checkForPasswordResetToken() {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        if (token && window.location.hash === '#reset-password') {
            getEl('reset-token-input').value = token;
            showModal(resetPasswordModal);
            // Clean up URL
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }

    function handleLogout() {
        state.isLoggedIn = false;
        state.user = null;
        localStorage.removeItem(TOKEN_KEY);
        updateAuthStateUI();
        advisorySection.classList.remove('hidden'); // Ensure advisory section is visible on logout
        dashboardSection.classList.add('hidden'); // Hide dashboard on logout
    }

    // ===================================================================
    // API HELPER
    // ===================================================================

    async function apiFetch(endpoint, options = {}, requiresAuth = true) {
        const headers = { 'Content-Type': 'application/json', ...options.headers };
        if (requiresAuth) {
            const token = localStorage.getItem(TOKEN_KEY);
            if (!token) throw new Error("Authentication required.");
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(endpoint, { ...options, headers });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || `Request failed with status ${response.status}`);
        return data;
    }

    // ===================================================================
    // TRANSLATION
    // ===================================================================

    function setLanguage(lang) {
        queryAll('[data-translate-key]').forEach(el => {
            const key = el.getAttribute('data-translate-key');
            if (translations[lang] && translations[lang][key]) {
                if (el.hasAttribute('data-translate-key-placeholder')) {
                     el.placeholder = translations[lang][key];
                } else {
                    el.textContent = translations[lang][key];
                }
            }
        });
    }

    // ===================================================================
    // ADVISORY FORM
    // ===================================================================

    function initAdvisoryForm() {
        // Fetch config from backend to populate dropdowns
        apiFetch('/config', {}, false)
            .then(config => {
                state.appConfig = config; // Store the config for later use
                const cropSelect = getEl('cropType');
                const soilSelect = getEl('soilType');

                // Capitalize helper
                const capitalize = s => s.charAt(0).toUpperCase() + s.slice(1);

                // Populate crops
                cropSelect.innerHTML = '<option value="">Select Crop</option>' + 
                    Object.keys(config.crops).sort().map(val => `<option value="${val}">${capitalize(val)}</option>`).join('');

                // Populate soils
                soilSelect.innerHTML = '<option value="">Select Soil</option>' + 
                    config.soil_types.map(val => `<option value="${val}">${capitalize(val)}</option>`).join('');
            })
            .catch(error => showAppError("Could not load form configuration. Please refresh."));
    }

    function handleCropTypeChange(e) {
        const cropStageSlider = getEl('cropStage');
        const cropStageLabels = getEl('crop-stage-labels');
        const selectedCrop = e.target.value;

        if (selectedCrop && state.appConfig && state.appConfig.crops[selectedCrop]) {
            cropStageSlider.disabled = false;
            const stages = state.appConfig.crops[selectedCrop].stages;
            const capitalize = s => s.charAt(0).toUpperCase() + s.slice(1);
            cropStageSlider.max = stages.length - 1; // Set slider max based on number of stages
            cropStageLabels.innerHTML = stages.map(stage => `<span>${capitalize(stage)}</span>`).join('');
            handleCropStageChange(); // Update progress bar
        } else {
            cropStageSlider.disabled = true;
            cropStageLabels.innerHTML = `<span class="text-center w-full" data-translate-key="stage_select_crop_first">Please select a crop first</span>`;
            getEl('stage-progress-bar').style.width = '0%';
        }
    }

    function handleCropStageChange() {
        const slider = getEl('cropStage');
        const progress = (slider.value / (slider.max - slider.min)) * 100;
        getEl('stage-progress-bar').style.width = `${progress}%`;
    }

    function handleGpsButtonClick() {
        const gpsStatus = getEl('gps-status');
        const mapContainer = getEl('map-container');

        if (!navigator.geolocation) {
            gpsStatus.textContent = "Geolocation is not supported by your browser.";
            return;
        }

        gpsStatus.textContent = "Detecting location...";
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                gpsStatus.textContent = `Lat: ${latitude.toFixed(4)}, Lon: ${longitude.toFixed(4)}`;
                mapContainer.classList.remove('hidden');
                
                if (state.map) {
                    state.map.setView([latitude, longitude], 13);
                } else {
                    state.map = L.map('map-container').setView([latitude, longitude], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(state.map);
                }

                if (state.mapMarker) {
                    state.mapMarker.setLatLng([latitude, longitude]);
                } else {
                    state.mapMarker = L.marker([latitude, longitude]).addTo(state.map);
                }
            },
            () => {
                gpsStatus.textContent = "Unable to retrieve your location. Please enter manually.";
            }
        );
    }

    async function handleAdvisoryFormSubmit(e) {
        e.preventDefault();
        if (!state.isLoggedIn) {
            showAppError("Please log in to get an advisory.");
            return;
        }

        const submitBtn = getEl('submit-btn');
        const btnText = getEl('submit-btn-text');
        const spinner = getEl('submit-spinner');

        btnText.textContent = 'Generating...';
        getEl('form-error').classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        // Construct the payload from form inputs
        const crop = getEl('cropType').value;
        const stageIndex = parseInt(getEl('cropStage').value, 10);
        const stage = state.appConfig.crops[crop].stages[stageIndex];

        const farmerInput = {
            name: getEl('farmerName').value,
            phone_number: getEl('phoneNumber').value,
            crop: crop,
            crop_stage: stage,
            soil_type: getEl('soilType').value,
            language: getEl('language-toggle').value, // Get the chosen language
            gps_location: {
                latitude: state.mapMarker ? state.mapMarker.getLatLng().lat : null,
                longitude: state.mapMarker ? state.mapMarker.getLatLng().lng : null,
            },
            enable_sms: getEl('enable_sms').checked,
            enable_whatsapp: getEl('enable_whatsapp').checked,
            enable_voice: getEl('enable_voice').checked,
        };

        try {
            const data = await apiFetch('/advisory/', {
                method: 'POST',
                body: JSON.stringify(farmerInput)
            });

            state.currentAdvisory = data.advisory;
            // Pass farmerInput to have access to cropName for the dashboard title
            displayDashboard(data.advisory, farmerInput);

        } catch (error) {
            const formError = getEl('form-error');
            formError.textContent = error.message;
            formError.classList.remove('hidden');
        } finally {
            btnText.textContent = 'Generate My Dashboard';
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    // Helper function to generate mock data based on input
    function clearAdvisoryForm() {
        advisoryForm.reset();
        getEl('stage-progress-bar').style.width = '0%';
        getEl('cropStage').disabled = true;
        getEl('crop-stage-labels').innerHTML = `<span class="text-center w-full" data-translate-key="stage_select_crop_first">Please select a crop first</span>`;
        if (state.map) {
            state.map.remove();
            state.map = null;
            state.mapMarker = null;
        }
        getEl('map-container').classList.add('hidden');
        getEl('gps-status').textContent = "Click the button to get your field's location.";
    }

    // ===================================================================
    // DASHBOARD
    // ===================================================================

    async function fetchMarketPrice(crop) {
        try {
            return await apiFetch(`/market-price/${crop}`);
        } catch (error) {
            console.error("Market price fetch error:", error);
            getEl('market-price-card').innerHTML = `<p class="text-center text-red-500">Could not load market data.</p>`;
            return null; // Return null on error
        }
    }
    async function displayDashboard(data, farmerInput) {
        advisorySection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
        window.scrollTo({ top: dashboardSection.offsetTop - 80, behavior: 'smooth' });
        const capitalize = s => s.charAt(0).toUpperCase() + s.slice(1);
        getEl('dashboard-crop-name').textContent = capitalize(farmerInput.crop);

        // Populate daily advice from weather
        const adviceContainer = getEl('daily-advice-container');
        adviceContainer.innerHTML = data.daily_advice ? `<p>${data.daily_advice}</p>` : `<p>Weather data could not be loaded. Please check your location and try again.</p>`;
        getEl('pest-recommendation-text').textContent = data.recommendation;
        
        // Populate schemes
        const schemesList = getEl('govt-schemes-list');
        schemesList.innerHTML = data.govt_schemes.map(scheme => 
            `<a href="${scheme.link}" target="_blank" class="block p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition">
                <span class="font-semibold text-primary-green">${scheme.name}</span>
                <p class="text-sm text-gray-600 mt-1">${scheme.description}</p>
            </a>`
        ).join('');

        // Populate weather
        const weatherContainer = getEl('weather-forecast-container');
        if (data.forecast && data.forecast.length > 0) {
            weatherContainer.innerHTML = data.forecast.map((day, index) => {
                const dayName = new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' });
                return `
                <div class="flex justify-between items-center p-2 bg-blue-50 rounded">
                    <span>${index === 0 ? 'Today' : dayName}</span>
                    <img src="https://openweathermap.org/img/wn/${day.icon}.png" alt="${day.description}" class="w-8 h-8">
                    <span class="font-semibold">${day.temp_min.toFixed(0)}° / ${day.temp_max.toFixed(0)}°C</span>
                </div>
            `}).join('');
        } else {
            weatherContainer.innerHTML = `<p class="text-gray-500">Forecast not available.</p>`;
        }

        // Populate Water Info
        if (data.water_info) {
            const availabilityEl = getEl('water-availability');
            availabilityEl.textContent = data.water_info.availability;
            availabilityEl.className = data.water_info.availability.toLowerCase().includes('good') ? 'font-bold text-green-600' : 'font-bold text-yellow-600';
            
            getEl('water-requirement').textContent = data.water_info.requirement || 'N/A';
            getEl('water-recommendation').textContent = data.water_info.recommendation;
        } else {
            getEl('water-info-container').innerHTML = `<p class="text-gray-500">Water information not available.</p>`;
        }

        // Populate crop health
        const cropHealthCard = getEl('crop-health-card');
        if (data.crop_health) {
            cropHealthCard.classList.remove('hidden');
            getEl('crop-health-status').textContent = data.crop_health.status;
            getEl('crop-health-ndvi').textContent = `NDVI: ${data.crop_health.ndvi.toFixed(2)}`;
            getEl('crop-health-message').textContent = data.crop_health.message;
        } else {
            cropHealthCard.classList.add('hidden');
        }

        // Populate soil health recommendation
        const soilHealthCard = getEl('soil-health-card');
        if (data.soil_recommendation) {
            soilHealthCard.classList.remove('hidden');
            getEl('soil-recommendation-text').textContent = data.soil_recommendation;
        } else {
            soilHealthCard.classList.add('hidden');
        }

        // Render Charts
        const riskMap = { "Low": 25, "Medium": 60, "High": 90 };
        const pestChartData = {
            labels: data.pest_predictions.map(p => p.pest),
            data: data.pest_predictions.map(p => riskMap[p.risk] || 10),
            risks: data.pest_predictions.map(p => p.risk) // Pass the risk levels to the chart renderer
        };
        renderPestChart(pestChartData);

        // Fetch and render the market price chart separately
        const marketData = await fetchMarketPrice(farmerInput.crop.toLowerCase());
        if (marketData && marketData.history) {
            const chartData = {
                labels: marketData.history.map(p => new Date(p.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })),
                data: marketData.history.map(p => p.price)
            };
            renderMarketPriceChart(chartData, marketData.unit);
        }
    }

    let pestChartInstance, marketChartInstance;

    function renderPestChart(chartData) {
        const ctx = getEl('pestPredictionChart').getContext('2d');
        if (pestChartInstance) pestChartInstance.destroy();

        // Define colors for different risk levels
        const riskColors = {
            "High": 'rgba(231, 111, 81, 0.8)', // accent-red
            "Medium": 'rgba(233, 196, 106, 0.8)', // accent-yellow
            "Low": 'rgba(42, 157, 143, 0.8)' // primary-green
        };
        const riskBorderColors = {
            "High": 'rgba(231, 111, 81, 1)',
            "Medium": 'rgba(233, 196, 106, 1)',
            "Low": 'rgba(42, 157, 143, 1)'
        };

        pestChartInstance = new Chart(ctx, {
            type: 'bar', // Changed from 'radar' to 'bar'
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Pest Risk (%)',
                    data: chartData.data,
                    // Dynamically set bar colors based on risk level
                    backgroundColor: chartData.risks.map(risk => riskColors[risk] || riskColors['Low']), // This line is now correct
                    borderColor: chartData.risks.map(risk => riskBorderColors[risk] || riskBorderColors['Low']), // This line is now correct
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y', // This makes it a horizontal bar chart
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false // Hide legend as the bar colors are self-explanatory
                    },
                    // Configure the new datalabels plugin
                    datalabels: {
                        anchor: 'end',
                        align: 'end',
                        offset: 8, // Add some space from the end of the bar
                        color: '#333', // Dark color for readability
                        font: {
                            weight: 'bold'
                        },
                        // This function returns the text to display (e.g., "High", "Medium")
                        formatter: (value, context) => chartData.risks[context.dataIndex]
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Risk Level'
                        }
                    }
                }
            }
        });
    }

    function renderMarketPriceChart(chartData, unit = 'INR/Quintal') {
        const ctx = getEl('marketPriceChart').getContext('2d');
        if (marketChartInstance) marketChartInstance.destroy();
        marketChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: `Price (${unit})`,
                    data: chartData.data,
                    backgroundColor: 'rgba(42, 157, 143, 0.8)'
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                tension: 0.1
            }
        });
    }

    // ===================================================================
    // HISTORY
    // ===================================================================
    
    async function showHistoryModal() {
        historyModalBackdrop.classList.remove('hidden');
        const container = getEl('history-list-container');
        container.innerHTML = `<div class="text-center text-gray-500 py-10" id="history-loading-spinner">
            <i class="fas fa-spinner fa-spin text-3xl"></i>
            <p class="mt-2" data-translate-key="history_loading">Loading history...</p>
        </div>`;
        
        try {
            const historyItems = await apiFetch('/advisories/history');
            renderHistory(historyItems);
        } catch (error) {
            container.innerHTML = `<p class="text-center text-red-500">Could not load history: ${error.message}</p>`;
        }
    }

    function renderHistory(historyItems) {
        const container = getEl('history-list-container');
        if (historyItems.length === 0) {
            container.innerHTML = `<p class="text-center text-gray-500 py-10">No advisory history found.</p>`;
            return;
        }
        container.innerHTML = historyItems.map(item => `
            <div class="p-4 border rounded-lg bg-white shadow-sm">
                <div class="flex justify-between items-center">
                    <h4 class="font-bold text-lg text-green-700">${item.crop}</h4>
                    <span class="text-sm text-gray-500">${new Date(item.date_sent).toLocaleString()}</span>
                </div>
                <p class="mt-2 text-gray-600 whitespace-pre-wrap">${item.advisory_text}</p>
            </div>
        `).join('');
    }

    // --- Run Initialization ---
    init();
});
