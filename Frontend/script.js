document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesDiv = document.getElementById('messages');
    const exampleItems = document.querySelectorAll('.examples li');
    
    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function displayEmployeeResults(results) {
        results.forEach(employee => {
            const card = document.createElement('div');
            card.classList.add('employee-card');
            
            let skillsHTML = employee.skills.map(skill => 
                `<span class="skill">${skill}</span>`
            ).join('');
            
            card.innerHTML = `
                <h3>${employee.name}</h3>
                <div><strong>Experience:</strong> ${employee.experience_years} years</div>
                <div><strong>Availability:</strong> ${employee.availability}</div>
                <div><strong>Projects:</strong> ${employee.past_projects.join(', ')}</div>
                <div class="skills">${skillsHTML}</div>
            `;
            
            messagesDiv.appendChild(card);
        });
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;
        
        addMessage(text, true);
        input.value = '';
        
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            if (data.results && data.results.length > 0) {
                displayEmployeeResults(data.results);
            } else {
                addMessage("Sorry, no matching employees found.", false);
            }
        } catch (error) {
            addMessage("Sorry, there was an error processing your request.", false);
            console.error('Error:', error);
        }
    }
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    exampleItems.forEach(item => {
        item.addEventListener('click', function() {
            input.value = this.textContent;
            sendMessage();
        });
    });
});
