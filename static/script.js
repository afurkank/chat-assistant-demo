document.addEventListener('DOMContentLoaded', () => {
    const fillForm = document.getElementById('fillForm');
    const changeBackground = document.getElementById('changeBackground');
    const gender = document.getElementById('gender');
    const personality = document.getElementById('personality');
    const avatarImage = document.getElementById('avatarImage');

    fillForm.addEventListener('click', () => {
        const formId = document.getElementById('formId').value;
        if (formId) {
            fetch('/update_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ formId: formId }),
            })
            .then(response => response.json())
            .then(data => {
                avatarImage.src = `data:image/png;base64,${data.avatar}`;
                document.body.style.backgroundImage = `url(data:image/png;base64,${data.background})`;
                console.log(data.message);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        } else {
            console.log('Please enter a Form ID');
        }
    });

    function updateAvatar() {
        fetch('/update_avatar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ gender: gender.value, personality: personality.value }),
        })
        .then(response => response.json())
        .then(data => {
            avatarImage.src = `data:image/png;base64,${data.avatar}`;
            console.log(data.message);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    gender.addEventListener('change', updateAvatar);
    personality.addEventListener('change', updateAvatar);

    changeBackground.addEventListener('click', () => {
        fetch('/change_background', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            document.body.style.backgroundImage = `url(data:image/png;base64,${data.background})`;
            console.log(data.message);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});