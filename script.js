// A simple markdown to HTML converter to render lists, bold, etc.
function simpleMarkdown(text) {
    let html = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italics
        .replace(/^- (.*?)(\n|$)/gm, '<li>$1</li>') // List items
        .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>') // Wrap lists in <ul>
        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>') // Code blocks
        .replace(/\n/g, '<br>'); // New lines
    return html;
}

document.addEventListener('DOMContentLoaded', () => {
    const codeInput = document.getElementById('codeInput');
    const submitBtn = document.getElementById('submitBtn');
    const chatWindow = document.getElementById('chatWindow');
    const typingIndicator = document.getElementById('thinkingOverlay'); // FIXED

    const handleSubmission = async () => {
        const userCode = codeInput.value.trim();
        if (!userCode) return;

        // 1. Display user's code
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'chat-message user-message';
        userMessageDiv.innerHTML = `<div class="message-content"><pre><code>${userCode.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre></div>`;
        chatWindow.appendChild(userMessageDiv);

        // Clear input and show typing animation
        codeInput.value = '';
        typingIndicator.style.display = 'flex';
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            // 2. Send code to backend
            const response = await fetch('/review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: userCode }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
