// Global variables
let currentMode = null;
let currentUserId = null;

// DOM Elements
const modeButtons = document.querySelectorAll('.mode-buttons button');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const voiceInput = document.getElementById('voice-input');
const sosButton = document.getElementById('sos-button');

// Speech Recognition Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
    };
}

// Event Listeners
modeButtons.forEach(button => {
    button.addEventListener('click', () => {
        currentMode = button.dataset.mode;
        modeButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        addMessage(`Mode changed to: ${currentMode}`, 'assistant');
    });
});

sendButton.addEventListener('click', handleSendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSendMessage();
    }
});

voiceInput.addEventListener('click', () => {
    if (recognition) {
        recognition.start();
    } else {
        alert('Speech recognition is not supported in your browser.');
    }
});

sosButton.addEventListener('click', handleSOS);

// Functions
async function handleSendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    if (!currentMode) {
        addMessage('Please select a mode first.', 'assistant');
        return;
    }

    addMessage(message, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/api/modes/' + currentMode, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                query: message
            })
        });

        const data = await response.json();
        if (response.ok) {
            addMessage(data.response, 'assistant');
        } else {
            addMessage('Error: ' + data.error, 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error processing your request.', 'assistant');
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleSOS() {
    if (!currentUserId) {
        alert('Please sign in first.');
        return;
    }

    try {
        const response = await fetch('/api/sos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId
            })
        });

        if (response.ok) {
            addMessage('Emergency services have been notified. Help is on the way.', 'assistant');
        } else {
            addMessage('Error sending SOS signal. Please try again or call emergency services directly.', 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Error sending SOS signal. Please call emergency services directly.', 'assistant');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is signed in
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
        currentUserId = storedUserId;
        addMessage('Welcome back! How can I help you today?', 'assistant');
    } else {
        // Redirect to signup if not signed in
        window.location.href = '/signup.html';
    }
}); 