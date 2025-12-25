// Get CSRF token from cookie (Django standard way)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Voting function
function voteIssue(issueId, voteType) {
    fetch(VOTE_URL_TEMPLATE.replace('0', issueId), {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `vote=${voteType}`
    })
    .then(response => response.json())
    .then(data => {
        const msgBox = document.getElementById(`vote-msg-${issueId}`);

        if (data.error) {
            msgBox.innerText = data.error;
            msgBox.style.color = "#dc2626";
        } else {
            document.getElementById(`real-count-${issueId}`).innerText = data.real;
            document.getElementById(`fake-count-${issueId}`).innerText = data.fake;
            msgBox.innerText = "✔ Vote recorded";
            msgBox.style.color = "#166534";
        }
    })
    .catch(() => {
        alert("Something went wrong. Try again.");
    });
}
