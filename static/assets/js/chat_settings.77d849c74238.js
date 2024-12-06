document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const temperatureSlider = document.querySelector('input[name="temperature"]');
    const maxLengthInput = document.querySelector('input[name="max_length"]');
    const contextMemoryInput = document.querySelector('input[name="context_memory"]');
    const modelSelect = document.querySelector('select[name="language_model"]');
    const languageSelect = document.querySelector('select[name="primary_language"]');
    const autoCorrectCheckbox = document.querySelector('input[name="auto_correct"]');
    const apiKeyInput = document.querySelector('input[name="api_key"]');
    const endpointUrlInput = document.querySelector('input[name="endpoint_url"]');

    // Load saved settings when page loads
    fetch('/chat/load_settings/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const settings = data.settings;
                
                // Update form fields with saved settings
                modelSelect.value = settings.model_name;
                temperatureSlider.value = settings.temperature;
                maxLengthInput.value = settings.max_length;
                contextMemoryInput.value = settings.context_memory;
                languageSelect.value = settings.language;
                autoCorrectCheckbox.checked = settings.auto_correct;
                apiKeyInput.value = settings.api_key;
                endpointUrlInput.value = settings.endpoint_url;

                // Update any visual displays
                updateTemperatureDisplay(settings.temperature);
            } else {
                console.error('Failed to load settings:', data.error);
            }
        })
        .catch(error => {
            console.error('Error loading settings:', error);
        });

    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        
        fetch('/chat/chat_settings/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                showNotification('Settings saved successfully!', 'success');
                
                // Optionally redirect
                setTimeout(() => {
                    window.location.href = '/chat/';
                }, 1500);
            } else {
                showNotification('Error saving settings: ' + data.error, 'error');
            }
        })
        .catch(error => {
            showNotification('Error saving settings', 'error');
            console.error('Error:', error);
        });
    });

    // Reset button handler
    document.querySelector('#reset-button').addEventListener('click', function() {
        // Default values
        temperatureSlider.value = 0.7;
        maxLengthInput.value = 500;
        contextMemoryInput.value = 5;
        modelSelect.value = 'phi3';
        languageSelect.value = 'English';
        autoCorrectCheckbox.checked = false;
        apiKeyInput.value = '';
        endpointUrlInput.value = '';
        
        updateTemperatureDisplay(0.7);
    });

    // Temperature slider visual feedback
    temperatureSlider.addEventListener('input', function() {
        updateTemperatureDisplay(this.value);
    });

    function updateTemperatureDisplay(value) {
        const temperatureDisplay = document.querySelector('#temperature-display');
        if (temperatureDisplay) {
            temperatureDisplay.textContent = value;
        }
    }

    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.textContent = message;
        
        const container = document.querySelector('.container');
        container.insertBefore(notification, container.firstChild);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
});