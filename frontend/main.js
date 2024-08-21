document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-like').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            handleAction(this, 'liked', 'unliked');
        });
    });

    document.querySelectorAll('.btn-dislike').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            handleAction(this, 'disliked', 'undisliked');
        });
    });

    document.querySelectorAll('.btn-follow').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            handleAction(this, 'followed', 'unfollowed');
        });
    });
});

function handleAction(button, actionTrue, actionFalse) {
    const url = button.getAttribute('href');

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.textContent = data.action === actionTrue ? actionFalse : actionTrue;
        }
    })
    .catch(error => console.error('Error:', error));
}
