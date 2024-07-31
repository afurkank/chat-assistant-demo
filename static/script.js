document.addEventListener('DOMContentLoaded', () => {
    const fillForm = document.getElementById('fillForm');
    const changeBackground = document.getElementById('changeBackground');
    const gender = document.getElementById('gender');
    const personality = document.getElementById('personality');
    const avatarImage = document.getElementById('avatarImage');
    const formLogo = document.getElementById('formLogo');
    const formTitle = document.getElementById('formTitle');

    fillForm.addEventListener('click', () => {
        const formId = document.getElementById('formId').value;
        if (formId) {
            fetch('/update_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ gender: gender.value, formID: formId }),
            })
            .then(response => response.json())
            .then(data => {
                avatarImage.src = `data:image/png;base64,${data.avatar}`;
                document.body.style.backgroundImage = `url(data:image/png;base64,${data.background})`;
                formLogo.src = `data:image/png;base64,${data.logo}`;
                formTitle.textContent = data.title;
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
        const formId = document.getElementById('formId').value;
        fetch('/update_avatar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ gender: gender.value, formID: formId }),
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
    // personality.addEventListener('change', updateAvatar); this is related to chat agent

    changeBackground.addEventListener('click', () => {
        const formId = document.getElementById('formId').value;
        fetch('/change_background', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ formID: formId }),
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