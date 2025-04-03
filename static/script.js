document.getElementById('input-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    const role = document.getElementById('role').value;
    const experience = document.getElementById('experience').value;
    const num_questions = document.getElementById('num_questions').value;

    // Send a POST request to the Flask API
    fetch('/process_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            role: role,
            experience: experience,
            num_questions: num_questions
        })
    })
    .then(response => response.json())
    .then(data => {
        // Clear previous results
        document.getElementById('questions-list').innerHTML = '';
        document.getElementById('tips').innerHTML = '';

        // Display questions
        if (data.questions.length === 0) {
            document.getElementById('questions-list').innerHTML = '<li>No questions available for this role.</li>';
        } else {
            data.questions.forEach(question => {
                const li = document.createElement('li');
                li.textContent = question;
                document.getElementById('questions-list').appendChild(li);
            });
        }

        // Display tips
        document.getElementById('tips').innerHTML = `
            <strong>Role-specific Tip:</strong> ${data.tips.role_tip}<br>
            <strong>Experience-specific Tip:</strong> ${data.tips.experience_tip}
        `;
    })
    .catch(error => console.error('Error:', error));
});
 