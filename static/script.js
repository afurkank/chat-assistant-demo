document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendMessage = document.getElementById('sendMessage');
    const fillForm = document.getElementById('fillForm');
    const changeBackground = document.getElementById('changeBackground');
    const gender = document.getElementById('gender');
    const personality = document.getElementById('personality');

    sendMessage.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            appendMessage('User', message);
            userInput.value = '';
            // Here you would typically send the message to the backend and get a response
            setTimeout(() => {
                appendMessage('Assistant', 'This is a placeholder response.');
            }, 1000);
        }
    });

    fillForm.addEventListener('click', () => {
        const formId = document.getElementById('formId').value;
        if (formId) {
            appendMessage('System', `Filling form with ID: ${formId}`);
            // Here you would typically send a request to the backend to fill the form
        } else {
            appendMessage('System', 'Please enter a Form ID');
        }
    });

    changeBackground.addEventListener('click', () => {
        appendMessage('System', 'Changing background...');
        // Here you would typically send a request to the backend to change the background
    });

    gender.addEventListener('change', () => {
        appendMessage('System', `Changed gender to: ${gender.value}`);
        // Here you would typically send a request to the backend to update the avatar
    });

    personality.addEventListener('change', () => {
        appendMessage('System', `Changed personality to: ${personality.value}`);
        // Here you would typically send a request to the backend to update the assistant's behavior
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});