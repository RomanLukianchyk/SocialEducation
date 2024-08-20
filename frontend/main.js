document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-like, .btn-dislike, .btn-follow').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.getAttribute('href');

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
                    // Обновляем текст кнопки в зависимости от действия
                    if (data.action === 'liked' || data.action === 'unliked') {
                        this.textContent = data.action === 'liked' ? 'Unlike' : 'Like';
                    } else if (data.action === 'disliked' || data.action === 'undisliked') {
                        this.textContent = data.action === 'disliked' ? 'Undislike' : 'Dislike';
                    } else if (data.action === 'followed' || data.action === 'unfollowed') {
                        this.textContent = data.action === 'followed' ? 'Unfollow' : 'Follow';
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
