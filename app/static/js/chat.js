const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
let history = [];

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const userMessage = messageInput.value.trim();

  if (!userMessage) return;

  // Show user message immediately
  addMessage('You', userMessage);
  messageInput.value = '';

  // Show a temporary "typing..." indicator
  const typingMessage = addMessage("Mom's Eye", 'Typing...');

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage, history: history }),
    });

    const data = await response.json();

    // Clean the "Typing..." message and replace with real reply
    typingMessage.innerHTML = `<strong>Mom's Eye:</strong> ${data.message || 'Sorry, no response.'}`;

    // Update history
    history = data.history;
  } catch (error) {
    typingMessage.innerHTML = `<strong>Mom's Eye:</strong> Error connecting to server.`;
    console.error('Chat error:', error);
  }
});

function addMessage(sender, message) {
  const messageElement = document.createElement('div');
  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatWindow.appendChild(messageElement);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return messageElement; // return element so we can modify later
}
